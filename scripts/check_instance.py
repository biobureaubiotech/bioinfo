# Boto 3
import boto3
ec2 = boto3.resource('ec2')

instances = ec2.instances.filter(
    Filters=[{'Name':'tag:Name', 'Values':['Bioinfo01']}])

for instance in instances:
    print(instance.public_ip_address,instance.platform,instance.public_dns_name);filters = [{'Name':'tag:Name', 'Values':['webapp01']}]