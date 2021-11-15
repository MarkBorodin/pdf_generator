# Generated by Django 3.1 on 2021-10-29 06:47

from django.db import migrations


def fill_in_the_field_title(apps, schema_editor):
    Offer = apps.get_model('pdf_generator', 'Offer')
    for offer in Offer.objects.all():
        if offer.title is None or offer.title == '':
            offer.title = 'Projekt'
            offer.save(update_fields=['title'])


def create_global_texts(apps, schema_editor):
    GlobalTexts = apps.get_model('pdf_generator', 'GlobalTexts')
    try:
        offerten = GlobalTexts.objects.get_or_create(
            name='Offerten',
            bottom_text='Es gelten die Allgemeinen Geschäftsbedingungen der Marketing Monkeys. Diese findest du unter:',
            url='https://www.marketingmonkeys.ch/agb/'
        )
        offerten.save()
    except Exception:
        pass
    try:
        rechnugen = GlobalTexts.objects.get_or_create(
            name='Rechnugen',
            bottom_text='Es gelten die Allgemeinen Geschäftsbedingungen der Marketing Monkeys. Diese findest du unter:',
            url='https://www.marketingmonkeys.ch/agb/'
        )
        rechnugen.save()
    except Exception:
        pass
    try:
        offer_confirmation = GlobalTexts.objects.get_or_create(
            name='Auftragsbestätigung',
            bottom_text="""Wir bedanken uns für den Auftrag und freuen uns auf eine erfolgreiche Zusammenarbeit. 
    Bitte senden Sie dieses Dokument gegengezeichnet an uns uruck.""",
        )
        offer_confirmation.save()
    except Exception:
        pass


def fill_in_the_field_global_texts(apps, schema_editor):
    Offer = apps.get_model('pdf_generator', 'Offer')
    Invoice = apps.get_model('pdf_generator', 'Invoice')
    OfferConfirmation = apps.get_model('pdf_generator', 'OfferConfirmation')
    GlobalTexts = apps.get_model('pdf_generator', 'GlobalTexts')
    for offer in Offer.objects.all():
        if offer.global_texts is None:
            offer.global_texts = GlobalTexts.objects.filter(name='Offerten')[0]
            offer.save()
    for invoice in Invoice.objects.all():
        if invoice.global_texts is None:
            invoice.global_texts = GlobalTexts.objects.filter(name='Rechnugen')[0]
            invoice.save()
    for offer_confirmation in OfferConfirmation.objects.all():
        if offer_confirmation.global_texts is None:
            offer_confirmation.global_texts = GlobalTexts.objects.filter(name='Auftragsbestätigung')[0]
            offer_confirmation.save()


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_generator', '0040_auto_20211028_1506'),
    ]

    operations = [
        migrations.RunPython(fill_in_the_field_title),
        migrations.RunPython(create_global_texts),
        migrations.RunPython(fill_in_the_field_global_texts),
    ]