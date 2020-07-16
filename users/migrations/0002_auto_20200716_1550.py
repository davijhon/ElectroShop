# Generated by Django 3.0.7 on 2020-07-16 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='payment_option',
            field=models.CharField(choices=[('S', 'Stripe'), ('P', 'Paypal')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='set_default_billing',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='set_default_shipping',
            field=models.BooleanField(default=False),
        ),
    ]
