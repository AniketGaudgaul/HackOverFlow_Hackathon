# Generated by Django 4.0 on 2022-05-08 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookweb', '0005_book_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='ISBN_number',
            field=models.IntegerField(),
        ),
    ]
