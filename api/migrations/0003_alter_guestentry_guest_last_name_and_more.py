# Generated by Django 4.0.4 on 2022-04-25 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_guestentry_guest_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guestentry',
            name='guest_last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='guestentry',
            name='keeper_full_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
