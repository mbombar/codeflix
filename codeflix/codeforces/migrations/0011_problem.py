# Generated by Django 3.0.2 on 2020-01-31 23:49

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeforces', '0010_auto_20200128_1501'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contest_id', models.IntegerField(null=True, verbose_name='Id of the contest containing the problem.')),
                ('problemset_name', models.CharField(max_length=255, null=True, verbose_name='Short name of the problemset the problem belongs to.')),
                ('index', models.CharField(max_length=255, verbose_name='Problem index in the contest.')),
                ('name', models.CharField(max_length=255, verbose_name='Name of the problem.')),
                ('type', models.CharField(choices=[('PROGRAMMING', 'PROGRAMMING'), ('QUESTION', 'QUESTION')], max_length=255, verbose_name='Type of the problem.')),
                ('points', models.FloatField(null=True, verbose_name='Maximum ammount of points for the problem.')),
                ('rating', models.IntegerField(null=True, verbose_name='Problem rating (difficulty).')),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), size=None, verbose_name='List of tags for the problem.')),
            ],
        ),
    ]
