# Generated by Django 3.0.1 on 2020-01-28 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeforces', '0005_auto_20200128_0027'),
    ]

    operations = [
        migrations.AddField(
            model_name='codeforcesuser',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Rating'),
        ),
    ]