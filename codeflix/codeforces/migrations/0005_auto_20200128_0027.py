# Generated by Django 3.0.1 on 2020-01-28 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeforces', '0004_auto_20200128_0025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='contest_id',
        ),
        migrations.AlterField(
            model_name='contest',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Id of the contest.'),
        ),
    ]
