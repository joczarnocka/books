# Generated by Django 3.2.5 on 2021-07-17 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booksapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="average_rating",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="book",
            name="ratings_count",
            field=models.IntegerField(null=True),
        ),
    ]
