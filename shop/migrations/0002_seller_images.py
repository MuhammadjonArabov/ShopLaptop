# Generated by Django 5.1.3 on 2024-12-13 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='seller_images/'),
        ),
    ]
