from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int
    )
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput
    )