# Generated by Django 3.0.10 on 2021-04-11 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_merge_20210411_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mentor',
            name='initials',
        ),
        migrations.AddField(
            model_name='user',
            name='initials',
            field=models.CharField(max_length=6, null=True),
        ),
    ]