# Generated by Django 4.1.4 on 2023-01-02 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("prof_stats", "0004_citiespercenttable_citiessalarytable_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="YearsGraph",
            fields=[
                (
                    "stat",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=100)),
                ("image", models.ImageField(upload_to="media/images/")),
            ],
        ),
        migrations.RenameModel(
            old_name="Graph",
            new_name="CitiesGraph",
        ),
    ]