# Generated by Django 3.1 on 2021-03-03 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_generator', '0008_offer_bemerkung'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('write_date', models.DateTimeField(auto_now=True, null=True)),
                ('number', models.PositiveSmallIntegerField(default=1)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='pdf_generator.offer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='designation',
            name='offer',
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('write_date', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.TextField(blank=True, default='phase', max_length=128, null=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phases', to='pdf_generator.page')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='designation',
            name='phase',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='designations', to='pdf_generator.phase'),
            preserve_default=False,
        ),
    ]
