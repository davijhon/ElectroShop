import django_filters
from django import forms
from django.db import models 
from .models import (
	Product,
	Category, 
	Brand,
	CamPixels,
	Storage,
)


class ProductFilter(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt', widget=forms.TextInput(attrs={
             'class':'form-control', 'type':"number"}), label='Minimum price')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt', widget=forms.TextInput(attrs={
             'class':'form-control', 'type':"number"}), label='Maximum price')
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
             'class':'mr-2 mt-1', 'type':"checkbox",}))         
    cam_pixels = django_filters.ModelMultipleChoiceFilter(queryset=CamPixels.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    storage = django_filters.ModelMultipleChoiceFilter(queryset=Storage.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Product
        fields = ['brand', 'storage', 'cam_pixels']