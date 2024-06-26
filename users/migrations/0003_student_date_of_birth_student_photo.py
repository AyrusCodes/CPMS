# Generated by Django 5.0.4 on 2024-05-13 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_company_alter_student_cv'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='photo',
            field=models.ImageField(null=True, upload_to='student_photos/photo.jpg'),
        ),
    ]
