# Generated by Django 4.0 on 2022-05-08 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookweb', '0006_alter_book_isbn_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='availability',
            field=models.CharField(choices=[('1', 'Exchange'), ('2', 'Lend'), ('3', 'Donate')], default='Exchange', max_length=20),
        ),
    ]
