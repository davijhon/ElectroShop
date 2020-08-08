# Generated by Django 3.0.7 on 2020-07-22 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'brand',
                'verbose_name_plural': 'brands',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='CamPixels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pixels', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'pixel',
                'verbose_name_plural': 'pixels',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_code', models.CharField(max_length=9)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField()),
                ('ordered', models.BooleanField(default=False)),
                ('user_billing_same_shipping', models.BooleanField(default=False)),
                ('being_delivered', models.BooleanField(default=False)),
                ('received', models.BooleanField(default=False)),
                ('refund_request', models.BooleanField(default=False)),
                ('refund_granted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-start_date',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_charge_id', models.CharField(max_length=50)),
                ('amount', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('available', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storage', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'storage',
                'verbose_name_plural': 'storages',
            },
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('accepted', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='products/%Y/%m/%d')),
                ('description', models.TextField(blank=True)),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField(default=1)),
                ('available', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Brand')),
                ('cam_pixels', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.CamPixels')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.Category')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Storage')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]