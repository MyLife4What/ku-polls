# Generated by Django 3.2.7 on 2021-09-18 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='ending date for voting'),
        ),
    ]
