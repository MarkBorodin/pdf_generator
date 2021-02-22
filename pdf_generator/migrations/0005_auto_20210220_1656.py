# Generated by Django 3.1 on 2021-02-20 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_generator', '0004_auto_20210219_2213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='billing_address',
        ),
        migrations.AddField(
            model_name='designation',
            name='name',
            field=models.TextField(max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='client_address',
            field=models.TextField(max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='client_name',
            field=models.TextField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='designation',
            name='description',
            field=models.TextField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='designation',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='offer',
            name='description',
            field=models.TextField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
