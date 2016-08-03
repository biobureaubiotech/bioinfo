from django import forms

import boto3

class UploadForm(forms.Form):
    file = forms.FileField(required=True)
    

# class ImportFileForm(forms.Form):

    # s3 = boto3.resource('s3')
    # files = []
    # for key in bucket.objects.filter(Prefix='input/'):
    #     files.append(key.key)
    # files = files[1:]

    # analysis_type = forms.ChoiceField(choices=CHOICES)
