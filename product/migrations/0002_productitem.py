# Generated by Django 2.2.7 on 2019-11-16 16:04

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gid', models.UUIDField(default=uuid.uuid4)),
                ('stock_in_date', models.DateTimeField()),
                ('stock_out_date', models.DateTimeField(null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.Product')),
            ],
        ),
    ]
