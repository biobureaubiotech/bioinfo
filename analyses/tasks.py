from celery.decorators import task
from django.conf import settings

from analyses.models import Analysis,Instance

from scripts.download_basespace import GetBaseSpaceLinks

import boto3
from boto3.s3.transfer import S3Transfer
from subprocess import call

from projects.models import Project, File

from django.core import serializers
import json
import os
from django.forms.models import model_to_dict
from time import sleep

def run_command(command):
    run_command = """ssh -o 'StrictHostKeyChecking=no' -t ubuntu@%s '%s'""" % (ip,command)
    output = call(run_command, shell=True)
    return(output)
def generate_link(key):
    s3 = boto3.client('s3')

    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 'bioinfobiobureau',
            'Key': key,
        },
        ExpiresIn=604800
    )
    return(url)    

@task(name="start_analysis")
def StartAnalysis(analysis_id):

    print('Start Analysis!')
    analysis = Analysis.objects.get(pk=analysis_id)
    project = Project.objects.get(pk=analysis.project.id)

    print(project)

    #prepare reads
    # prepare_fastq(analysis, project)
    #assembly
    assembly(analysis, project)
    print('Finished Analysis')


def prepare_fastq(analysis, project):
    global ip
    #download fastq
    #check if instance exists getinstance or create one
    try:
        instance = Instance.objects.get(analysis=analysis.id)
    except Instance.DoesNotExist:
        instance_type = 'c4.large'
        instance = start_instance(analysis.id, instance_type)
        #wait until status change
        print('its running!!!')
    
    command = "scp -o 'StrictHostKeyChecking=no' $HOME/.s3cfg ubuntu@%s:~/" % (instance.ip_address)
    output = call(command, shell=True)

    #connect to instance
    print(instance.ip_address)

    #prepare environment
    path = '%s/data/analyses/%s' % (settings.ROOT_DIR, analysis.id)

    if not os.path.exists(path):
        os.makedirs(path)

    os.chdir(path)

    call("cp %s/scripts/run_analysis.py ." % (settings.ROOT_DIR), shell=True)

    #generate download links
    s3 = boto3.client('s3')
    file_id = analysis.parameters['file']
    file = File.objects.get(pk=file_id)

    
    key = 'input/%s' % (file.key)

    #prepare information

    parameters = {}
    parameters['analysis'] = model_to_dict( analysis )
    parameters['instance'] = model_to_dict( instance )
    parameters['aws'] = []
    
    file_dict= {} 
    # file_dict['link'] = generate_link(key)
    file_dict['name'] = file.key

    parameters['aws'].append(file_dict)

    # json_data = model_to_dict( parameters )

    with open('parameters.json', 'w') as outfile:
        json.dump(parameters, outfile, indent=4, sort_keys=True)

    #run script

    #run some analysis
    
    ip = instance.ip_address
    #transfer files to instance
    # command = "rsync -avz . ubuntu@%s:
    
    remote_path = "analysis_%s" % (analysis.id)
    
    command = "mkdir -p %s" % (remote_path)
    output = run_command(command)

    command = "rsync -avz . ubuntu@%s:~/%s" % (ip, remote_path)
    output = call(command, shell=True)

    print(output)
    # print(output)
    command = "cd %s;python run_analysis.py" % (remote_path)
    output = run_command(command)
    print(output)

def assembly(analysis, project):
    global ip

    print('Start Assembly')

    #download fastq
    #check if instance exists getinstance or create one
    try:
        instance = Instance.objects.get(analysis=analysis.id)
    except Instance.DoesNotExist:
        instance_type = 'r3.large'
        instance = start_instance(analysis.id, instance_type)
        #wait until status change
        print('its running!!!')
    
    command = "scp -o 'StrictHostKeyChecking=no' $HOME/.s3cfg ubuntu@%s:~/" % (instance.ip_address)
    output = call(command, shell=True)

    #connect to instance
    print(instance.ip_address)

    #prepare environment
    path = '%s/data/analyses/%s' % (settings.ROOT_DIR, analysis.id)

    if not os.path.exists(path):
        os.makedirs(path)

    os.chdir(path)

    call("cp %s/scripts/workflows/run_assembly.py ." % (settings.ROOT_DIR), shell=True)

    #generate download links
    s3 = boto3.client('s3')
    file_id = analysis.parameters['file']
    file = File.objects.get(pk=file_id)

    
    key = 'input/%s' % (file.key)

    #prepare information

    parameters = {}
    parameters['analysis'] = model_to_dict( analysis )
    parameters['instance'] = model_to_dict( instance )
    parameters['aws'] = []
    
    file_dict= {} 
    # file_dict['link'] = generate_link(key)
    file_dict['name'] = file.key

    parameters['aws'].append(file_dict)

    # json_data = model_to_dict( parameters )

    with open('parameters.json', 'w') as outfile:
        json.dump(parameters, outfile, indent=4, sort_keys=True)

    #run script

    #run some analysis
    
    ip = instance.ip_address
    #transfer files to instance
    # command = "rsync -avz . ubuntu@%s:
    
    remote_path = "analysis_%s" % (analysis.id)
    
    command = "mkdir -p %s" % (remote_path)
    output = run_command(command)

    command = "rsync -avz . ubuntu@%s:~/%s" % (ip, remote_path)
    output = call(command, shell=True)

    print(output)
    # print(output)
    command = "cd %s;python run_assembly.py" % (remote_path)
    output = run_command(command)
    print(output)

def start_instance(analysis_id,instance_type):

    print('Starting Instance...')

    analysis = Analysis.objects.get(pk=analysis_id)
    project = Project.objects.get(pk=analysis.project.id)


    instance = Instance()
    instance.project = project
    instance.analysis = analysis
    
    instance.user = project.user
    instance.status = 'new'
    instance.save()

    ec2 = boto3.resource('ec2')
    instances = ec2.create_instances(
        ImageId='ami-2d39803a', 
        MinCount=1, 
        MaxCount=1,
        InstanceType=instance_type,#t2.nano
        KeyName='bioinfo_biobureau',
        BlockDeviceMappings=[
            {
                # 'VirtualName': 'BioinfoHD',
                'DeviceName': '/dev/sda1',#xvdb
                'Ebs': {

                    'VolumeSize': 300,
                    'DeleteOnTermination': True,
                    'VolumeType': 'gp2',
                },
                # 'NoDevice': 'string'
            },
        ],
        )
    aws_instance = instances[0]
    tag = aws_instance.create_tags(
        Tags=[
            {
                'Key': 'Name',
                'Value': 'BioinfoImporter'
            },
        ]
    )

    aws_instance.wait_until_running()
    sleep(60) #
    instance.instance_id = aws_instance.instance_id
    instance.ip_address = aws_instance.public_ip_address
    instance.status = 'running'
    instance.save()
    print('Instance Started!!!')
    return(instance)

@task(name="stop_instance")
def stop_instance(instance_id):
    print('Stopping Instance...', instance_id)
    instance = Instance.objects.get(pk=instance_id)
    aws_instanceid = instance.instance_id
    ec2 = boto3.resource('ec2')
    ids = [aws_instanceid]
    ec2.instances.filter(InstanceIds=ids).stop()
    instance.status = 'stopped'
    instance.save()

@task(name="terminate_instance")
def terminate_instance(instance_id):
    print('Terminating Instance...', instance_id)
    instance = Instance.objects.get(pk=instance_id)
    aws_instanceid = instance.instance_id
    ec2 = boto3.resource('ec2')
    ids = [aws_instanceid]
    ec2.instances.filter(InstanceIds=ids).terminate()
    instance.status = 'terminated'
    instance.save()
