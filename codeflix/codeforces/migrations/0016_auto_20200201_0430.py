# Generated by Django 3.0.2 on 2020-02-01 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeforces', '0015_auto_20200201_0300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codeforcesuser',
            name='max_rating',
            field=models.IntegerField(blank=True, verbose_name='Max Rating'),
        ),
    ]
