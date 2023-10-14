# Generated by Django 4.2.6 on 2023-10-14 23:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salesmetrics', '0006_change_sale_payment_method_relationship_to_one_to_many'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='salesmetrics.location'),
        ),
    ]