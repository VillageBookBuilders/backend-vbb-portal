# Generated by Django 3.0.10 on 2021-07-20 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0018_auto_20210429_1940"),
        ("program", "0013_auto_20210429_1940"),
    ]

    operations = [
        migrations.AlterField(
            model_name="headmastersprogramassociation",
            name="headmaster",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="program_headmaster", to="users.Headmaster"),
        ),
        migrations.AlterField(
            model_name="program",
            name="headmasters",
            field=models.ManyToManyField(through="program.HeadmastersProgramAssociation", to="users.Headmaster"),
        ),
        migrations.AlterField(
            model_name="program",
            name="notes",
            field=models.TextField(blank=True, help_text="comments, suggestions, notes, events, open-house dates,            mentor program break dates, internet connectivity, power avalibility,            state of infrastructure, etc", null=True),
        ),
        migrations.AddConstraint(
            model_name="mentorslotassociation",
            constraint=models.UniqueConstraint(condition=models.Q(deleted=False), fields=("mentor", "slot"), name="unique_mentor_slot_pair"),
        ),
    ]
