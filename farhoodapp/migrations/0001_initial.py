# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-10 13:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('good', 'Good'), ('bad', 'Bad'), ('worst', 'Worst')], default='good', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('type', models.CharField(choices=[('coffee', 'Coffee'), ('bear', 'Bear'), ('shopping', 'Shopping'), ('dinning', 'Dinning'), ('logo', 'Logo'), ('sports', 'Sports')], default='coffee', max_length=150)),
                ('description', models.CharField(max_length=150)),
                ('scheduled_time', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('location_name', models.CharField(max_length=150)),
                ('location_address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='EventMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follow', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farhoodapp.Event')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('image', models.ImageField(null=True, upload_to='images/')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('nick_name', models.CharField(max_length=150)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('account_id', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=150)),
                ('temporary_profile', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_superuser', models.BooleanField(default=True, help_text='Designates whether this user should be treated as super user or not . Unselect this instead of deleting accounts.', verbose_name='superuser')),
                ('ref_user', models.ManyToManyField(blank=True, related_name='_user_ref_user_+', to='farhoodapp.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='eventmember',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farhoodapp.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farhoodapp.Event'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farhoodapp.User'),
        ),
        migrations.AddField(
            model_name='action',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farhoodapp.Event'),
        ),
        migrations.AddField(
            model_name='action',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farhoodapp.User'),
        ),
    ]
