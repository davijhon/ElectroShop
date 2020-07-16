from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


ADDRESS_CHOICES = (

	('B', 'Billing'),
	('S', 'Shipping'),

)


class CustomUser(AbstractUser):
	pass


class UserProfile(models.Model):
	user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
	shipping_address = models.CharField(max_length=255, blank=True, null=True)
	shipping_address2 = models.CharField(max_length=255, blank=True, null=True)
	shipping_country = CountryField(multiple=False)
	shipping_zip = models.CharField(max_length=50, blank=True, null=True)


	billing_address = models.CharField(max_length=255, blank=True, null=True)
	billing_address2 = models.CharField(max_length=255, blank=True, null=True)
	billing_country = CountryField(multiple=False, blank=True, null=True)
	billing_zip = models.CharField(max_length=255, blank=True, null=True)
	address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES )
	default = models.BooleanField(default=False)
	same_address_billing = models.BooleanField(default=False)


	def __str__(self):
		return self.user.username

	def user_name(self):
		return self.user.first_name + ' ' + self.user.last_name

