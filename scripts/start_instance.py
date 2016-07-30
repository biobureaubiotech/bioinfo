#http://boto3.readthedocs.io/en/latest/guide/migrationec2.html#launching-new-instances
#http://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Subnet.create_instances
#http://www.ec2instances.info/

# Boto 3
import boto3
ec2 = boto3.resource('ec2')

# Boto 3
#Ubuntu Server 14.04 LTS (HVM), SSD Volume Type - ami-2d39803a
instances = ec2.create_instances(
    ImageId='ami-2d39803a', 
    MinCount=1, 
    MaxCount=1,
    InstanceType='t2.nano',
    KeyName='bioinfo_biobureau',
    BlockDeviceMappings=[
        {
            # 'VirtualName': 'BioinfoHD',
            'DeviceName': '/dev/sda1',#xvdb
            'Ebs': {

                'VolumeSize': 10,
                'DeleteOnTermination': True,
                'VolumeType': 'gp2',
            },
            # 'NoDevice': 'string'
        },
    ],
    )
instance = instances[0]

tag = instance.create_tags(
    Tags=[
        {
            'Key': 'Name',
            'Value': 'Bioinfo01'
        },
    ]
)

print(instance)
print(instance.instance_id, instance.public_ip_address)


