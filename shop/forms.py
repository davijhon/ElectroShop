from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget



class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()
