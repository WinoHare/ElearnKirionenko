# Generated by Django 4.1.4 on 2023-01-02 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("prof_stats", "0005_yearsgraph_rename_graph_citiesgraph"),
    ]

    operations = [
        migrations.CreateModel(
            name="SkillsGraph",
            fields=[
                (
                    "stat",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=100)),
                ("image", models.ImageField(upload_to="media/images/")),
            ],
        ),
        migrations.CreateModel(
            name="SkillsTable",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("skill", models.CharField(max_length=30)),
                ("count", models.IntegerField()),
            ],
        ),
    ]