# Generated by Django 3.0.10 on 2021-03-20 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20210320_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newslettersubscriber',
            name='subscriber_type',
            field=models.CharField(choices=[(10, 'REGISTRATION'), (20, 'VBB_NEWSLETTER')], default=20, max_length=254),
        ),
    ]