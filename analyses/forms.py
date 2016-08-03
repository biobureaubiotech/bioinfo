from django import forms

CHOICES = (('plant_assembly_pipeline', 'Plant Assembly Pipeline',), ('2', 'Second Pipeline',))

class AnalysisForm(forms.Form):
    name = forms.CharField(label='Analysis Name', max_length=100) 
    analysis_type = forms.ChoiceField(choices=CHOICES)
    description = forms.CharField(widget=forms.Textarea)