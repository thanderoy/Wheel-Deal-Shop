# Generated by Django 4.2.1 on 2023-09-09 18:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0004_translations"),
    ]

    operations = [
        migrations.AlterField(
            model_name="producttranslation",
            name="slug",
            field=models.SlugField(max_length=200),
        ),
    ]
