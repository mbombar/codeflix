# Generated by Django 3.0.1 on 2020-01-28 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeforces', '0003_contest_useful'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='difficulty',
            field=models.IntegerField(null=True, verbose_name='Larger number means more difficult problems'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='relative_time_seconds',
            field=models.BigIntegerField(null=True, verbose_name='Number of seconds, passed after the start of the contest.'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='start_time_seconds',
            field=models.BigIntegerField(null=True, verbose_name='Contest start time in unix format.'),
        ),
    ]
