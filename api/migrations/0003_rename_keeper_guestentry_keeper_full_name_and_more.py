# Generated by Django 4.0.4 on 2022-04-14 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_guestentry_exit_datetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guestentry',
            old_name='keeper',
            new_name='keeper_full_name',
        ),
        migrations.AlterField(
            model_name='guestentry',
            name='notes',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
