# Generated by Django 5.0.4 on 2024-05-15 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_remove_notification_student_notification_student_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='student_id',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
