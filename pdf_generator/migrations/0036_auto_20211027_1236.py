# Generated by Django 3.1 on 2021-10-27 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_generator', '0035_auto_20210908_0920'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalTexts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('write_date', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=128)),
                ('bottom_text', models.TextField(blank=True, default='Es gelten die Allgemeinen Geschäftsbedingungen der Marketing Monkeys. Diese findest du unter: ', max_length=256, null=True)),
                ('url', models.TextField(blank=True, default='https://www.marketingmonkeys.ch/agb/', max_length=128, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='invoice',
            name='global_texts',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to='pdf_generator.globaltexts'),
        ),
        migrations.AddField(
            model_name='offer',
            name='global_texts',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offers', to='pdf_generator.globaltexts'),
        ),
        migrations.AddField(
            model_name='offerconfirmation',
            name='global_texts',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offer_confirmations', to='pdf_generator.globaltexts'),
        ),
    ]
