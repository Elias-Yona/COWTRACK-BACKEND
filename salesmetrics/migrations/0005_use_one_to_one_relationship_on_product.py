# Generated by Django 4.2.6 on 2023-10-14 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salesmetrics', '0004_make_serial_number_nullable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='salesmetrics.product'),
        ),
    ]
