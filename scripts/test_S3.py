import boto3
s3 = boto3.resource('s3')

bucket = s3.Bucket('bioinfobiobureau')
print(bucket)

# files = s3.Bucket('bioinfobiobureau').objects.filter(Prefix='input')
# # print(bucket)
# for file in files:
#     print(file) 

# for bucket in s3.buckets.all():
#     print(bucket.name)
files = []
for key in bucket.objects.filter(Prefix='input/'):
    # print(key.key)
    files.append(key.key)
print(files[1:])    
# files = bucket.objects.filter(Prefix='input/')
