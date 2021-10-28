# Generated by Django 3.1 on 2021-10-28 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_generator', '0038_auto_20211027_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='title',
            field=models.TextField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='designation',
            name='description',
            field=models.TextField(max_length=256, null=True),
        ),
    ]
