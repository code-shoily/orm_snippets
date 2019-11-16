# Generated by Django 2.2.7 on 2019-11-16 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(auto_now=True, db_index=True)),
                ('sender', models.CharField(max_length=127)),
                ('recipient', models.CharField(max_length=127)),
            ],
        ),
    ]
