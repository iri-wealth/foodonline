# Generated by Django 4.2.6 on 2023-10-23 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_vendor_vendor_slug_alter_vendor_vendor_license'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='vendor_slug',
            field=models.SlugField(default=0, max_length=55, unique=True),
        ),
    ]
