# Generated by Django 3.2.6 on 2021-08-26 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210825_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='ImageList',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.imagelist'),
        ),
    ]
