#http://boto3.readthedocs.io/en/latest/guide/migrationec2.html#launching-new-instances
#http://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Subnet.create_instances
#http://www.ec2instances.info/

# Boto 3
import boto3
import argparse

ec2 = boto3.resource('ec2')

parser = argparse.ArgumentParser(description='Terminate Instance')
parser.add_argument('-i','--input', help='instance_id', required=True)
args = parser.parse_args()
# print args
input_file = args.input

# Boto 3
ids = [input_file]
ec2.instances.filter(InstanceIds=ids).stop()
ec2.instances.filter(InstanceIds=ids).terminate()



# [ec2.Instance(id='i-2db6c5b3')]
