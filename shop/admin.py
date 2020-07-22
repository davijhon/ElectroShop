from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe


from .models import (
	Product, OrderItem, Order,
	 Payment, Refund, 
	Category, Brand, CamPixels,
	Storage, Brand, Promo
)


def order_detail(obj):
	return mark_safe('<a href="{}">View</a>'.format(
		reverse('shop:admin_order_detail', args=[obj.id])
	))


def make_refund_accepted(modeladmin, request, queryset):
	queryset.update(refund_request=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'




@admin.register(CamPixels)
class CamPixelsAdmin(admin.ModelAdmin):
	list_display = ['pixels',]


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
	list_display = ['storage',]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug',]
	prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = [
			'name', 
			'slug', 
			'price',
			'available', 
			'created', 
			'updated'
	]
	list_filter = ['available', 'created', 'updated']
	list_editable = ['price', 'available']
	prepopulated_fields = {'slug': ('name',)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = [
			'id',
			'user', 
			'ordered', 
			'being_delivered',
			'received',
			'refund_request',
			'refund_granted',
			'payment',
			'shipping_billing_info',
			'user_billing_same_shipping',
			order_detail,
	]
	list_filter = [
			'user', 
			'ordered', 
			'being_delivered',
			'received',
			'refund_request',
			'refund_granted',
	]

	list_display_links = [
			#'user', 
			'shipping_billing_info',
			'payment',
	]
	search_fields = [
		'user__username',
		'ref_code',
	]
	actions = [make_refund_accepted]


#admin.site.register(OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Refund)
admin.site.register(Promo)