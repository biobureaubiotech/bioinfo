from django import forms

class AnalysisForm(forms.Form):
    name = forms.CharField(label='Analysis Name', max_length=100) 