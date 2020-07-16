from django.contrib.auth import get_user_model
from django import forms 
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


from .models import UserProfile


PAYMENT_CHOICES = (
	('S', 'Stripe'),
	('P', 'Paypal'),
)



class CustomUserCreationForm(UserCreationForm):

	class Meta:
		model = get_user_model()
		fields = ('email', 'username',)
		widgets = {
          'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email Address'}),
		  'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
		

class CustomUserChangeForm(UserChangeForm):

	class Meta:
		model = get_user_model()
		fields = ('email', 'username',)


class ProfileEditForm(forms.ModelForm):
	shipping_address = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder':'Street address',
		'class': 'form-control',
	}))
	shipping_address2 = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder':'Apartment, suite, unit etc. (optional)',
		'class': 'form-control',
	}))
	shipping_country = CountryField(blank_label='(select country').formfield(
		required=False,
		widget=CountrySelectWidget(attrs={
			'class': 'custom-select d-block w-100',
			}))
	shipping_zip = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder':'Zip Code',
		'class': 'form-control',
	}))


	billing_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
		'placeholder':'Street address',
		'class': 'form-control',
	}))
	billing_address2 = forms.CharField(required=False ,widget=forms.TextInput(attrs={
		'placeholder':'Apartment, suite, unit etc. (optional)',
		'class': 'form-control',
	}))
	billing_country = CountryField(blank_label='(select country').formfield(
		required=False,
		widget=CountrySelectWidget(attrs={
			'class': 'custom-select d-block w-100',
			}))
	billing_zip = forms.CharField(required=False ,widget=forms.TextInput(attrs={
		'placeholder':'Zip Code',
		'class': 'form-control',
	}))
	
	# same_address_billing = forms.BooleanField(widget=forms.CheckboxInput(attrs={
	# 	'input_type': 'checkbox',
	# 	'class': 'custom-checkbox'	
	# 	#'class': 'custom-control-input',
		
	# }))

	class Meta:
		model = UserProfile
		fields = ('shipping_address', 'shipping_address2', 'shipping_country', 'shipping_zip',
					'billing_address', 'billing_address2', 'billing_country', 'billing_zip',
					'same_address_billing',)


