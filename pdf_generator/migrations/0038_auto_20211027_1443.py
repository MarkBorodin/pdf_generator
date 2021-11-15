# Generated by Django 3.1 on 2021-10-27 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_generator', '0037_auto_20211027_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='designation',
            name='fixed_price',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='designation',
            name='quantity',
            field=models.SmallIntegerField(default=0),
        ),
    ]