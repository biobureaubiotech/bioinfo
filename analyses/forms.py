from django import forms
from projects.models import File
from django.forms import ModelForm
from .models import Analysis

CHOICES = (
	('gbs_se', 'Genotype By Sequencing - Single End',), 
	('gbs_pe', 'Genotype By Sequencing - Paired End',)
	)

class AnalysisForm(forms.Form):
    # name = forms.CharField(label='Analysis Name', max_length=100) 
    analysis_type = forms.ChoiceField(choices=CHOICES)
    # description = forms.CharField(widget=forms.Textarea)

#GBSFormSE
class AnalysisGBSSEForm(ModelForm):
    # name = forms.CharField(label='Analysis Name', max_length=100) 
    file = forms.ModelChoiceField(label="FASTQ", queryset=File.objects.all()) 
    barcodes = forms.CharField(widget=forms.Textarea)
    adapters = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Analysis
        fields = ['name', 'description']
    
    def __init__(self, *args, **kwargs):
        self.project_id = kwargs.pop('project_id', None)
        super(AnalysisGBSSEForm, self).__init__(*args, **kwargs)
        self.fields['file'] = forms.ModelChoiceField(label="FASTQ", queryset=File.objects.filter(project=self.project_id)) 
        self.fields.keyOrder = [
            'name',
            'description',
            'file',
            'barcodes',
            'adapters'
            ]