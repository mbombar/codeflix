# Generated by Django 2.2.3 on 2020-02-01 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codeforces', '0017_auto_20200201_0432'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codeforcesuser',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='codeforcesuser',
            name='city',
        ),
        migrations.RemoveField(
            model_name='codeforcesuser',
            name='contribution',
        ),
        migrations.RemoveField(
            model_name='codeforcesuser',
            name='country',
        ),
        migrations.RemoveField(
            model_name='codeforcesuser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='codeforcesuser',
            name='friend_of_count',
        ),
        migrations.RemoveField(
            model_name='codeforcesuser',
            name='last_online_time_seconds',
        ),
        migrations.RemoveField(
            model_name='codeforcesuser',
            name='max_rank',
        ),
        migrations.RemoveField(
            model_name='codeforcesuser',
            name='max_rating',
        ),
        migrations.RemoveField(
            model_name='codeforcesuser',
            name='open_id',
        ),
        migrations.RemoveField(
            model_name='codeforcesuser',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='codeforcesuser',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='codeforcesuser',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='codeforcesuser',
            name='registration_time_seconds',
        ),
        migrations.RemoveField(
            model_name='codeforcesuser',
            name='title_photo',
        ),
        migrations.RemoveField(
            model_name='codeforcesuser',
            name='vk_id',
        ),
    ]
