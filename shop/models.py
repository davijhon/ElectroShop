from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django.db import models 
from django.urls import reverse
# MPTT.FIELDS IMPORT TreeForeignKey -> pip install django-mptt

from users.models import UserProfile



class Promo(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length=120)
	image = models.ImageField(blank=True, upload_to='images/')
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name


#              MPTT.Models
class Category(models.Model):
	# parent = TreeForeignKey('self', blank=True, null=True, related_name='childen', on_delete=models.CASCADE)
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=200)
	image = models.ImageField(blank=True, upload_to='images/')
	slug = models.SlugField(max_length=200, unique=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'
		
	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('shop:categories', kwargs={'slug': self.slug})
	

class Brand(models.Model):
	name = models.CharField(max_length=100)
	image = models.ImageField(blank=True, upload_to='images/')
	slug = models.SlugField(max_length=100, unique=True)
	category = models.ForeignKey(Category,
									related_name='brands',
									on_delete=models.CASCADE)

	class Meta:
		ordering = ('name',)
		verbose_name = 'brand'
		verbose_name_plural = 'brands'
	
	def __str__(self):
		return self.name


class CamPixels(models.Model):
	pixels = models.CharField(max_length=50, blank=True, null=True)

	class Meta:
		verbose_name = 'pixel'
		verbose_name_plural = 'pixels'
	
	def __str__(self):
		return self.pixels


class Storage(models.Model):
	storage = models.CharField(max_length=50, blank=True, null=True)

	class Meta:
		verbose_name = 'storage'
		verbose_name_plural = 'storages'
	
	def __str__(self):
		return self.storage


class Product(models.Model):
	category = models.ForeignKey(Category,
									related_name='products',
									on_delete=models.CASCADE)
	brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(max_length=200, db_index=True)
	image = models.ImageField(upload_to='products/%Y/%m/%d',
							blank=True)
	description = models.TextField(blank=True)
	cam_pixels = models.ForeignKey(CamPixels, on_delete=models.CASCADE)
	storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
	price = models.FloatField()
	quantity = models.IntegerField(default=1)
	available = models.BooleanField(default=True)
	featured = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	
	class Meta:
		ordering = ('name',)
		index_together = (('id', 'slug'),)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:produtc-detail', kwargs={'slug': self.slug})

	def get_add_to_cart_url(self):
		return reverse("shop:add-to-cart", kwargs={
				'slug': self.slug
		})

	def get_remove_from_cart_url(self):
		return reverse("shop:remove-from-cart", kwargs={
				'slug': self.slug
		})

class OrderItem(models.Model):
	user = models.ForeignKey(get_user_model(),
							 on_delete=models.CASCADE,)
	ordered = models.BooleanField(default=False)
	item = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)


	def __str__(self):
		return f"{self.quantity} of {self.item.name}"

	def get_total_items_price(self):
		return self.quantity * self.item.price

	def get_final_price(self):
		return self.get_total_items_price()

#related_name='billing_address'
#related_name='shipping_address'
class Order(models.Model):
	user = models.ForeignKey(get_user_model(),
							 on_delete=models.CASCADE)
	ref_code = models.CharField(max_length=9)
	items = models.ManyToManyField(OrderItem)
	start_date = models.DateTimeField(auto_now_add=True)
	ordered_date = models.DateTimeField()
	ordered = models.BooleanField(default=False)
	# billing_address = models.ForeignKey(
	# 	UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
	# shipping_address = models.ForeignKey(
	# 	UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
	payment = models.ForeignKey(
		'Payment', on_delete=models.SET_NULL, blank=True, null=True,
	)

	being_delivered = models.BooleanField(default=False)
	received = models.BooleanField(default=False)
	refund_request = models.BooleanField(default=False)
	refund_granted = models.BooleanField(default=False)


	def __str__(self):
		return self.user.username


	def get_total(self):
		total = 0
		for order_item in self.items.all():
			total += order_item.get_final_price()
		return total


class Payment(models.Model):
	stripe_charge_id = models.CharField(max_length=50)
	user = models.ForeignKey(get_user_model(), 
							on_delete=models.SET_NULL, blank=True, null=True)
	amount = models.FloatField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username


class Refund(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	reason = models.TextField()
	accepted = models.BooleanField(default=False)
	email = models.EmailField()

	def __str__(self):
		return f"{self.pk}"



