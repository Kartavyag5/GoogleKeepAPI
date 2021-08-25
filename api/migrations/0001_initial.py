# Generated by Django 3.2.6 on 2021-08-25 12:04

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(default='Image-list', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(default='Task-list', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=50)),
                ('Labels', models.CharField(max_length=30)),
                ('Background_color', models.CharField(choices=[('white', 'White'), ('red', 'Red'), ('orange', 'Orange'), ('yellow', 'Yellow'), ('green', 'Green'), ('blue', 'Blue'), ('purple', 'Purple'), ('black', 'Black')], default='white', max_length=20)),
                ('Description', models.TextField()),
                ('Reminder', models.DateTimeField(default=None)),
                ('Created_at', models.DateTimeField(auto_now_add=True)),
                ('Updated_at', models.DateTimeField(auto_now=True)),
                ('ImageList', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.imagelist')),
                ('List', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.list')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Task', models.CharField(default='task', max_length=30)),
                ('Done', models.BooleanField(default=False)),
                ('List', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.list')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(default='notes/default.jpg', upload_to=api.models.user_directory_path2)),
                ('ImageList', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.imagelist')),
            ],
        ),
        migrations.CreateModel(
            name='Extendeduser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Profile', models.ImageField(default='notes/default.jpg', upload_to=api.models.user_directory_path)),
                ('Phone', models.CharField(max_length=15)),
                ('Created_at', models.DateTimeField(auto_now_add=True)),
                ('Updated_at', models.DateTimeField(auto_now=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
