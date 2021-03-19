from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from pdf_generator.models import Designation, Page, Phase, Offer, Invoice


@receiver(post_save, sender=Phase)
def phase_number(sender, instance, created, **kwargs):
    if created:
        phases_num = Phase.objects.filter(
            page__in=Page.objects.filter(offer=instance.page.offer)
        ).count()
        instance.number = phases_num
        instance.save()


@receiver(post_save, sender=Designation)
def designations_number(sender, instance, created, **kwargs):
    if created:
        designations_num = Designation.objects.filter(
            phase=instance.phase
        ).count()
        instance.number = designations_num
        instance.save()


@receiver(post_save, sender=Offer)
def invoice_update(sender, instance, created, **kwargs):
    if created is False:
        invoice = Invoice.objects.get(offer=instance, number=instance.number)
        invoice.client_address = instance.client_address
        invoice.client_name = instance.client_name
        invoice.email = instance.email
        invoice.description = instance.description
        invoice.iban = instance.iban
        invoice.bic_swift = instance.bic_swift
        invoice.kontonummer = instance.kontonummer
        invoice.bemerkung = instance.bemerkung
        invoice.zahlbar_bis = instance.create_date + timedelta(days=30)
        invoice.netto_price = instance.get_netto_price()
        invoice.mwst = instance.get_mwst()
        invoice.invoice_amount_total = instance.get_invoice_amount_total()
        invoice.create_date = instance.create_date
        invoice.save()
