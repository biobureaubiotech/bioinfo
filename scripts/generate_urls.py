import boto3
import requests

# Get the service client.
s3 = boto3.client('s3')


files = ['WorkingFiles/Petrobras01/Arquivos Blast To Megan/R_2013_11_30_15_23_49_user_CTL-148-Metagenoma_Mauro_Eduardo2.CTLT_PGM.IonXpress_001_Q20_TrimRL_AT_80pb_cdhit97.blast_output.gz', 'WorkingFiles/Petrobras01/Arquivos Blast To Megan/R_2013_11_30_15_23_49_user_CTL-148-Metagenoma_Mauro_Eduardo2.CTLT_PGM.IonXpress_002_Q20_TrimRL_AT_80pb_cdhit97.blast_output.gz', 'WorkingFiles/Petrobras01/Arquivos Blast To Megan/R_2013_11_30_15_23_49_user_CTL-148-Metagenoma_Mauro_Eduardo2.CTLT_PGM.IonXpress_003_Q20_TrimRL_AT_80pb_cdhit97.blast_output.gz', 'WorkingFiles/Petrobras01/Arquivos Blast To Megan/R_2013_11_30_15_23_49_user_CTL-148-Metagenoma_Mauro_Eduardo2.CTLT_PGM.IonXpress_004_Q20_TrimRL_AT_80pb_cdhit97.blast_output.gz', 'WorkingFiles/Petrobras01/Arquivos Blast To Megan/R_2013_11_30_15_23_49_user_CTL-148-Metagenoma_Mauro_Eduardo2.CTLT_PGM.IonXpress_005_Q20_TrimRL_AT_80pb_cdhit97.blast_output.gz', 'WorkingFiles/Petrobras01/Arquivos Blast To Megan/R_2013_11_30_15_23_49_user_CTL-148-Metagenoma_Mauro_Eduardo2.CTLT_PGM.IonXpress_006_Q20_TrimRL_AT_80pb_cdhit97.blast_output.gz', 'WorkingFiles/Petrobras01/Arquivos Blast To Megan/R_2013_11_30_15_23_49_user_CTL-148-Metagenoma_Mauro_Eduardo2.CTLT_PGM.IonXpress_007_Q20_TrimRL_AT_80pb_cdhit97.blast_output.gz', 'WorkingFiles/Petrobras01/Arquivos Blast To Megan/R_2013_11_30_15_23_49_user_CTL-148-Metagenoma_Mauro_Eduardo2.CTLT_PGM.IonXpress_008_Q20_TrimRL_AT_80pb_cdhit97.blast_output.gz', 'WorkingFiles/Petrobras01/Arquivos Blast To Megan/R_2013_11_30_15_23_49_user_CTL-148-Metagenoma_Mauro_Eduardo2.CTLT_PGM.IonXpress_009_Q20_TrimRL_AT_80pb_cdhit97.blast_output.gz', 'WorkingFiles/Petrobras01/Arquivos Blast To Megan/R_2013_11_30_15_23_49_user_CTL-148-Metagenoma_Mauro_Eduardo2.CTLT_PGM.IonXpress_010_Q20_TrimRL_AT_80pb_cdhit97.blast_output.gz', 'WorkingFiles/Petrobras01/Arquivos Blast To Megan/R_2013_11_30_15_23_49_user_CTL-148-Metagenoma_Mauro_Eduardo2.CTLT_PGM.IonXpress_011_Q20_TrimRL_AT_80pb_cdhit97.blast_output.gz', 'WorkingFiles/Petrobras01/Arquivos Blast To Megan/R_2013_11_30_15_23_49_user_CTL-148-Metagenoma_Mauro_Eduardo2.CTLT_PGM.IonXpress_012_Q20_TrimRL_AT_80pb_cdhit97.blast_output.gz', 'WorkingFiles/Petrobras01/Arquivos Blast To Megan/R_2013_11_30_15_23_49_user_CTL-148-Metagenoma_Mauro_Eduardo2.CTLT_PGM.IonXpress_013_Q20_TrimRL_AT_80pb_cdhit97.blast_output.gz', 'WorkingFiles/Petrobras01/Arquivos Blast To Megan/R_2013_11_30_15_23_49_user_CTL-148-Metagenoma_Mauro_Eduardo2.CTLT_PGM.IonXpress_014_Q20_TrimRL_AT_80pb_cdhit97.blast_output.gz', 'WorkingFiles/Petrobras01/Arquivos Blast To Megan/R_2013_11_30_15_23_49_user_CTL-148-Metagenoma_Mauro_Eduardo2.CTLT_PGM.IonXpress_015_Q20_TrimRL_AT_80pb_cdhit97.blast_output.gz']

for file in files:
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 's3biobureau01',
            'Key': file,
        },
        ExpiresIn=604800
    )
    print(url)
    print('\n')

#http://stackoverflow.com/questions/17831535/how-to-generate-file-link-without-expiry


# Generate the URL to get 'key-name' from 'bucket-name'


# import boto3
# s3 = boto3.resource('s3')

# for bucket in s3.buckets.all():
#     print(bucket.name)
#     # for key in bucket.objects.all():
#     #     print(key.key)