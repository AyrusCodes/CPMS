# Generated by Django 5.0.4 on 2024-05-15 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_rename_job_posting_appliedcandidates_job_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobposting',
            name='status',
            field=models.CharField(default='open', max_length=20),
        ),
        migrations.AlterField(
            model_name='jobposting',
            name='company_id',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
