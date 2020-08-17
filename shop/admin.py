from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin


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

def export_to_csv(modeladmin, request, queryset):
	opts = modeladmin.model._meta
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
	writer = csv.writer(response)

	fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
	# Write a first row with header information
	writer.writerow([field.verbose_name for field in fields])
	# Write data rows
	for obj in queryset:
		data_row = []
		for field in fields:
			value = getattr(obj, field.name)
			if isinstance(value, datetime.datetime):
				value = value.strftime('%d/%m/%Y')
			data_row.append(value)
		writer.writerow(data_row)
	return response

export_to_csv.short_description = 'Export to CSV'



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


# class CategoryAdmin2(DraggableMPTTAdmin):
#     mptt_indent_field = "name"

#     list_display = ('tree_actions', 'indented_title', 'related_products_count', 'related_products_cumulative_count')
#     list_display_links = ('indented_title',)

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)

#         # Add cumulative product count
#         qs = Category.objects.add_related_count(
#                 qs,
#                 Product,
#                 'category',
#                 'products_cumulative_count',
#                 cumulative=True)

#         # Add non cumulative product count
#         qs = Category.objects.add_related_count(qs,
#                  Product,
#                  'category',
#                  'products_count',
#                  cumulative=False)
#         return qs

#     def related_products_count(self, instance):
#         return instance.products_count
#     related_products_count.short_description = 'Related products (for this specific category)'

#     def related_products_cumulative_count(self, instance):
#         return instance.products_cumulative_count
#     related_products_cumulative_count.short_description = 'Related products (in tree)'


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
	actions = [make_refund_accepted, export_to_csv]


# admin.site.register(Category, CategoryAdmin2)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Refund)
admin.site.register(Promo)