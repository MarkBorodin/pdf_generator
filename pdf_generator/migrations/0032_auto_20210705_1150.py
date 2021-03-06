# Generated by Django 3.1 on 2021-07-05 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_generator', '0031_offerconfirmation_schlusstext'),
    ]

    operations = [
        migrations.CreateModel(
            name='HourlyRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('write_date', models.DateTimeField(auto_now=True, null=True)),
                ('rate', models.FloatField(default=30, null=True)),
                ('name', models.TextField(blank=True, max_length=256, null=True)),
            ],
            options={
                'verbose_name': 'hourly rate',
                'verbose_name_plural': 'hourly rate',
                'ordering': ['-create_date'],
            },
        ),
        migrations.AddField(
            model_name='designation',
            name='number_of_hours',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='designation',
            name='price',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='designations', to='pdf_generator.hourlyrate'),
        ),
    ]
