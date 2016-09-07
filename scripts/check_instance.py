# Boto 3
import boto3
ec2 = boto3.resource('ec2')

# instances = ec2.instances.filter(
#     Filters=[{'Name':'tag:Name', 'Values':['BioinfoImporter']}])

instances = ec2.instances.filter(InstanceIds=['i-1766dd26'])
aws_instance = list(instances)[0]

print(aws_instance)
print(dir(aws_instance))
print(aws_instance.public_ip_address)
print(aws_instance.state)

# for instance in instances:
#     print(dir(instance))
#     print(instance.id, instance.instance_type, instance.report_status)
#     print(instance.public_ip_address)

#	print(instance.public_ip_address,instance.platform,instance.public_dns_name)
    #;filters = [{'Name':'tag:Name', 'Values':['webapp01']}]

# for status in ec2.meta.client.describe_instance_status()['InstanceStatuses']:
#     print(status)