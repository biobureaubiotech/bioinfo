from celery.decorators import task
from django.conf import settings

from projects.models import AlignmentFile, AlignmentHit, Project, File

from projects.models import Task as ProjectTask
from analyses.models import Instance

import zipfile

from django import db
from django.db import transaction

import sys
import os

from scripts.download_basespace import GetBaseSpaceLinks

import boto3
from boto3.s3.transfer import S3Transfer
from subprocess import call

@task(name="process_task")
def process_task(project_task_id):
    
    project_task = ProjectTask.objects.get(pk=project_task_id)
    
    if project_task.task_type == 'import_from_basespace':
        import_files_from_basespace(project_task.id)


def import_files_from_basespace(task_id):

    s3 = boto3.resource('s3')
    client = boto3.client('s3')
    transfer = S3Transfer(client)

    bucket = s3.Bucket('bioinfobiobureau')

    print('Import Files from BaseSpace')
    project_task = ProjectTask.objects.get(pk=task_id)

    
    projects = project_task.task_data['projects']
    
    # #download from basespace
    basespace = GetBaseSpaceLinks(projects)
    files = basespace.getfilelinks()

    print('path', os.getcwd())
    download_path = '../work/projects/%s/tasks/%s/' % (project_task.project.id, project_task.id)
    
    if not os.path.isdir(download_path):
        os.makedirs(download_path)
    os.chdir(download_path)

    print('path', os.getcwd())

    #download files
    for file in files:
        #check if file exists
        if not os.path.isfile(file):
            command = 'wget -O %s %s' % (file, files[file])
            output = call(command, shell=True)

        #upload to S3

        key ='input/%s' % (file)
        # Upload a new file
        objs = list(bucket.objects.filter(Prefix=key))
        if len(objs) > 0 and objs[0].key == key:
            print("Exists!")
        else:
            print("Doesn't exist")
            transfer.upload_file(file, 'bioinfobiobureau', key)
            print('%s sent to S3!' % (file))
            #create File object
        file_obj = File()
        file_obj.user = project_task.user
        file_obj.name = file
        file_obj.project = project_task.project
        file_obj.save()


    #upload files to S3


    #turn on machine
    # start_instance(project_task.project.id)
    #download data from BaseSpace
    #upload data to S3
    #turn off machine


def add_prefix(file_id):
    print('Adding Prefix')
    file = File.objects.get(pk=file_id)
    


# def start_instance(project_id):

#     print('Starting Instance...')

#     project = Project.objects.get(pk=project_id)

#     instance = Instance()
#     instance.project = project
#     instance.user = project.user
#     instance.status = 'new'
#     instance.save()

#     ec2 = boto3.resource('ec2')
#     instances = ec2.create_instances(
#         ImageId='ami-2d39803a', 
#         MinCount=1, 
#         MaxCount=1,
#         InstanceType='t2.nano',
#         KeyName='bioinfo_biobureau',
#         BlockDeviceMappings=[
#             {
#                 # 'VirtualName': 'BioinfoHD',
#                 'DeviceName': '/dev/sda1',#xvdb
#                 'Ebs': {

#                     'VolumeSize': 100,
#                     'DeleteOnTermination': True,
#                     'VolumeType': 'gp2',
#                 },
#                 # 'NoDevice': 'string'
#             },
#         ],
#         )
#     aws_instance = instances[0]
#     tag = aws_instance.create_tags(
#         Tags=[
#             {
#                 'Key': 'Name',
#                 'Value': 'BioinfoImporter'
#             },
#         ]
#     )
#     instance.instance_id = aws_instance.instance_id
#     instance.ip_address = aws_instance.public_ip_address
#     instance.status = 'running'
#     instance.save()
#     print('Instance Started!!!')
#     # return(instance)


@task(name="start_instance")
def start_instance(instance_id):
    print('Starting Instance...', instance_id)
    instance = Instance.objects.get(pk=instance_id)
    aws_instanceid = instance.instance_id
    ec2 = boto3.resource('ec2')
    ids = [aws_instanceid]
    ec2.instances.filter(InstanceIds=ids).start()
    instances = ec2.instances.filter(InstanceIds=ids)
    aws_instance = list(instances)[0]
    aws_instance.wait_until_running()
    instances = ec2.instances.filter(InstanceIds=ids)
    aws_instance = list(instances)[0]
    print(aws_instance)
    print(dir(aws_instance))
    print(aws_instance.public_ip_address)
    print(aws_instance.state)
    instance.ip_address = aws_instance.public_ip_address
    instance.status = 'running'
    instance.save()
    print('Instance Started!!!')


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

@task(name="import_alignment_to_database")
def import_alignment(alignment_file_id):
    
    print('Import FILE', alignment_file_id)

    aln_file = AlignmentFile.objects.get(pk=alignment_file_id)
    #delete hits from files before inserting
    AlignmentHit.objects.filter(alnfile=aln_file).delete()

    print(aln_file.alnfile)

    full_path = '%s/%s' % (settings.MEDIA_ROOT, aln_file.alnfile)

    if aln_file.name.endswith('.zip'):
        archive = zipfile.ZipFile(full_path, 'r')
        filename = archive.namelist()[0]
        infile = archive.open(filename, 'r')

    else:
        infile = open(full_path, 'r')

    count = 0
    
    
    hits = []
    for line in infile:
        
        count += 1

        # bulk insert variants objects
        if count == 50000:
            # with transaction.atomic():
            # print("Inserting ...")
            AlignmentHit.objects.bulk_create(hits)
            # db.reset_queries()
            # print ' Done!'
            count = 0
            del hits
            hits = []
        

        hit = line.decode('utf-8').split('\t')

        # if len(hit) < 16:
        #     diff = 16 - len(hit)
        #     for i in range(0,2):
        #         hit.append('')

        # print(hit)
        # print(len(hit))

        # if len(hit) < 19:
        #     diff = 19 - len(hit)
        #     # print diff
        #     for i in range(0,diff):
        #         hit.append('')

        if hit[0] != 'qseqid':
            
            aln_hit = AlignmentHit()
            aln_hit.project = aln_file.project
            aln_hit.alnfile = aln_file

            aln_hit.qseqid = hit[0]
            aln_hit.sseqid = hit[1]
            aln_hit.pident = hit[2]
            aln_hit.length = hit[3]
            aln_hit.mismatch = hit[4]
            aln_hit.gapopen = hit[5]
            aln_hit.qstart = hit[6]
            aln_hit.qend = hit[7]
            aln_hit.sstart = hit[8]
            aln_hit.send = hit[9]
            aln_hit.evalue = hit[10]
            aln_hit.bitscore = hit[11]
            aln_hit.GI = hit[12]
            aln_hit.GeneID = hit[13]
            aln_hit.NCBI_taxon_of_the_reference = hit[14]
            aln_hit.Lowest_taxon_of_the_cluster = hit[15]
            aln_hit.RepID = hit[16]
            aln_hit.Cluster_Name = hit[17]
            # aln_hit.go_terms = hit[18]

            # aln_hit.save()
            hits.append(aln_hit)

    # with transaction.atomic():
    # print("Inserting Final...")
    AlignmentHit.objects.bulk_create(hits)
    # db.reset_queries()
    del hits

    
    aln_file.status = 'inserted'
    aln_file.save()
    print('Finished!')