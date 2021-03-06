# Generated by Django 3.2.9 on 2021-11-04 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20211104_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
