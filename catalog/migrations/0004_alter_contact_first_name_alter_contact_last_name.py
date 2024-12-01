# Generated by Django 5.1.1 on 2024-10-01 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0003_contact"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="first_name",
            field=models.CharField(max_length=150, verbose_name="Имя"),
        ),
        migrations.AlterField(
            model_name="contact",
            name="last_name",
            field=models.CharField(max_length=150, verbose_name="Фамилия"),
        ),
    ]
