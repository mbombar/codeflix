# Generated by Django 3.0.2 on 2020-02-14 23:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codeforces', '0018_auto_20200201_0509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codeforcesuser',
            name='database_user',
        ),
    ]
