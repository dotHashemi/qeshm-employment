# Generated by Django 3.1.5 on 2021-01-12 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_account_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='verify',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
