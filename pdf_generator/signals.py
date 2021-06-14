from datetime import timedelta

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from pdf_generator.models import Designation, Page, Phase, Offer, Invoice, OfferConfirmation, Signature
from pdf_generator.utils import image_to_code


@receiver(post_save, sender=Signature)
def get_code_from_image(sender, instance, created, **kwargs):
    if created:
        obj = Signature.objects.get(id=instance.id)
        obj.image_code = image_to_code(instance.image)
        obj.save()


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
        try:
            invoice = Invoice.objects.get(offer=instance, number=instance.number)
            invoice.client_address = instance.client_address
            invoice.client_name = instance.client_name
            invoice.email = instance.email
            invoice.description = instance.description
            invoice.iban = instance.payment_information.iban
            invoice.bic_swift = instance.payment_information.bic_swift
            invoice.kontonummer = instance.payment_information.kontonummer
            invoice.bemerkung = instance.bemerkung
            invoice.zahlbar_bis = instance.create_date + timedelta(days=30)
            invoice.netto_price = instance.get_netto_price()
            invoice.mwst = instance.get_mwst()
            invoice.invoice_amount_total = instance.get_invoice_amount_total()
            invoice.create_date = instance.create_date
            invoice.category = instance.category
            invoice.save()
        except Invoice.DoesNotExist:
            pass


@receiver(post_save, sender=Offer)
def offer_confirmation_update(sender, instance, created, **kwargs):
    if created is False:
        try:
            offer_confirmation = OfferConfirmation.objects.get(offer=instance, number=instance.number)
            offer_confirmation.client_address = instance.client_address
            offer_confirmation.client_name = instance.client_name
            offer_confirmation.email = instance.email
            offer_confirmation.description = instance.description
            offer_confirmation.iban = instance.payment_information.iban
            offer_confirmation.bic_swift = instance.payment_information.bic_swift
            offer_confirmation.kontonummer = instance.payment_information.kontonummer
            offer_confirmation.bemerkung = instance.bemerkung
            offer_confirmation.zahlbar_bis = instance.create_date + timedelta(days=30)
            offer_confirmation.netto_price = instance.get_netto_price()
            offer_confirmation.mwst = instance.get_mwst()
            offer_confirmation.invoice_amount_total = instance.get_invoice_amount_total()
            offer_confirmation.create_date = instance.create_date
            offer_confirmation.category = instance.category
            offer_confirmation.save()
        except OfferConfirmation.DoesNotExist:
            pass


@receiver(post_delete, sender=Offer)
@receiver(post_save, sender=Offer)
@receiver(post_delete, sender=Page)
@receiver(post_save, sender=Page)
@receiver(post_delete, sender=Phase)
@receiver(post_save, sender=Phase)
@receiver(post_delete, sender=Designation)
@receiver(post_save, sender=Designation)
def update_invoice_offer_confirmation(sender, instance, **kwargs):
    try:
        if sender is Designation:
            offer = Offer.objects.get(number=instance.phase.page.offer.number)
        elif sender is Phase:
            offer = Offer.objects.get(number=instance.page.offer.number)
        elif sender is Page:
            offer = Offer.objects.get(number=instance.offer.number)
        elif sender is Offer:
            offer = Offer.objects.get(number=instance.number)
    except Exception as e:
        print(e)
    try:
        invoice = Invoice.objects.get(offer=offer, number=offer.number)
        invoice.client_address = offer.client_address
        invoice.client_name = offer.client_name
        invoice.email = offer.email
        invoice.description = offer.description
        invoice.iban = offer.payment_information.iban
        invoice.bic_swift = offer.payment_information.bic_swift
        invoice.kontonummer = offer.payment_information.kontonummer
        invoice.bemerkung = offer.bemerkung
        invoice.zahlbar_bis = offer.create_date + timedelta(days=30)
        invoice.netto_price = offer.get_netto_price()
        invoice.mwst = offer.get_mwst()
        invoice.invoice_amount_total = offer.get_invoice_amount_total()
        invoice.create_date = offer.create_date
        invoice.category = offer.category
        invoice.save()

        offer_confirmation = OfferConfirmation.objects.get(offer=offer, number=offer.number)
        offer_confirmation.client_address = offer.client_address
        offer_confirmation.client_name = offer.client_name
        offer_confirmation.email = offer.email
        offer_confirmation.description = offer.description
        offer_confirmation.iban = offer.payment_information.iban
        offer_confirmation.bic_swift = offer.payment_information.bic_swift
        offer_confirmation.kontonummer = offer.payment_information.kontonummer
        offer_confirmation.bemerkung = offer.bemerkung
        offer_confirmation.zahlbar_bis = offer.create_date + timedelta(days=30)
        offer_confirmation.netto_price = offer.get_netto_price()
        offer_confirmation.mwst = offer.get_mwst()
        offer_confirmation.invoice_amount_total = offer.get_invoice_amount_total()
        offer_confirmation.create_date = offer.create_date
        offer_confirmation.category = offer.category
        offer_confirmation.save()
    except Exception as e:
        print(e)
