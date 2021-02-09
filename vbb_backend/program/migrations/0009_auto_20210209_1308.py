# Generated by Django 3.0.10 on 2021-02-09 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210209_0849'),
        ('program', '0008_auto_20210209_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentorslotassociation',
            name='mentor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mentor_slot', to='users.Mentor'),
        ),
        migrations.AlterField(
            model_name='mentorslotassociation',
            name='slot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='slot_mentor', to='program.Slot'),
        ),
        migrations.AlterField(
            model_name='studentslotassociation',
            name='slot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='slot_student', to='program.Slot'),
        ),
        migrations.AlterField(
            model_name='studentslotassociation',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_slot', to='users.Student'),
        ),
    ]
