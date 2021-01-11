# Generated by Django 3.1.5 on 2021-01-11 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0003_auto_20210111_0944'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisement',
            old_name='status',
            new_name='isActive',
        ),
        migrations.AddField(
            model_name='advertisement',
            name='isVerified',
            field=models.BooleanField(default=False),
        ),
    ]