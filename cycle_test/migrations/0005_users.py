# Generated by Django 4.2.7 on 2024-08-14 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cycle_test', '0004_cycletestdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(max_length=50)),
            ],
        ),
    ]
