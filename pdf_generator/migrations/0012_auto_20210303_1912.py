# Generated by Django 3.1 on 2021-03-03 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_generator', '0011_auto_20210303_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='bemerkung',
            field=models.TextField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='bic_swift',
            field=models.TextField(default='CRESCHZZ80A', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='client_address',
            field=models.TextField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='client_name',
            field=models.TextField(max_length=128, null=True),
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
        migrations.AlterField(
            model_name='offer',
            name='iban',
            field=models.TextField(default='CH26 0483 5216 7077 3100 0', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='kontonummer',
            field=models.TextField(default='2167077-32', max_length=32, null=True),
        ),
    ]
