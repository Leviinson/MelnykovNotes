# Generated by Django 4.1.3 on 2022-11-18 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='description',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
