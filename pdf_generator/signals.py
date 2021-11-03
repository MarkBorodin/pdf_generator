from datetime import timedelta

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from pdf_generator.models import Designation, Page, Phase, Offer, Invoice, OfferConfirmation, Signature
from pdf_generator.utils import image_to_code

from functools import wraps


def skip_signal():
    def _skip_signal(signal_func):
        @wraps(signal_func)
        def _decorator(sender, instance, **kwargs):
            if hasattr(instance, 'skip_signal'):
                return None
            return signal_func(sender, instance, **kwargs)
        return _decorator
    return _skip_signal


@receiver(post_save, sender=Signature)
def get_code_from_image(sender, instance, created, **kwargs):
    if created:
        obj = Signature.objects.get(id=instance.id)
        obj.image_code = image_to_code(instance.image)
        obj.save()


@receiver(post_save, sender=Phase)
@skip_signal()
def phase_number(sender, instance, created, **kwargs):
    if created is False:
        phases = Phase.objects.filter(page__in=Page.objects.filter(offer=instance.page.offer), name=instance.name)
        unique_phase = False if phases.count() > 1 else True
        if not unique_phase:
            instance.number = phases[0].number
            instance.main = False
        else:
            instance.number = Phase.objects.filter(page__in=Page.objects.filter(offer=instance.page.offer), main=True).count() # noqa
        instance.skip_signal = True
        instance.save()
        instance.skip_signal = False


@receiver(post_delete, sender=Phase)
@skip_signal()
def phases_number_delete(sender, instance, **kwargs):
    try:
        phases = Phase.objects.filter(page__in=Page.objects.filter(offer=instance.page.offer))
        counter = 1
        for phase in phases:
            if phase.main:
                phase.number = counter
                counter = counter + 1
            else:
                phase.number = Phase.objects.filter(page__in=Page.objects.filter(offer=instance.page.offer), name=phase.name)[0].number # noqa
            phase.skip_signal = True
            phase.save()
            phase.skip_signal = False
    except Exception as e:
        with open('log.txt', 'w') as f:
            f.write(str(e))


@receiver(post_delete, sender=Designation)
def designations_number_delete(sender, instance, **kwargs):
    try:
        current_phase = instance.phase
        phases = Phase.objects.filter(
            page__in=Page.objects.filter(offer=current_phase.page.offer),
            name=current_phase.name)
        counter = 1
        for phase in phases:
            for designation in phase.designations.all():
                designation.number = counter
                designation.save()
                counter = counter + 1
    except Exception as e:
        with open('log.txt', 'w') as f:
            f.write(str(e))


@receiver(post_save, sender=Offer)
def invoice_update(sender, instance, created, **kwargs):
    if created is False:
        try:
            invoice = Invoice.objects.get(offer=instance, number=instance.number)
            invoice.client_address = instance.client_address
            invoice.client_name = instance.client_name
            invoice.email = instance.email
            invoice.title = instance.title
            invoice.description = instance.description
            invoice.iban = instance.payment_information.iban
            invoice.bic_swift = instance.payment_information.bic_swift
            invoice.kontonummer = instance.payment_information.kontonummer
            invoice.bemerkung = instance.bemerkung
            # invoice.zahlbar_bis = instance.create_date + timedelta(days=30)
            invoice.netto_price = instance.get_netto_price()
            invoice.mwst = instance.get_mwst()
            invoice.invoice_amount_total = instance.get_invoice_amount_total()
            # invoice.create_date = instance.create_date
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
            offer_confirmation.title = instance.title
            offer_confirmation.description = instance.description
            offer_confirmation.iban = instance.payment_information.iban
            offer_confirmation.bic_swift = instance.payment_information.bic_swift
            offer_confirmation.kontonummer = instance.payment_information.kontonummer
            offer_confirmation.bemerkung = instance.bemerkung
            # offer_confirmation.zahlbar_bis = instance.create_date + timedelta(days=30)
            offer_confirmation.netto_price = instance.get_netto_price()
            offer_confirmation.mwst = instance.get_mwst()
            offer_confirmation.invoice_amount_total = instance.get_invoice_amount_total()
            # offer_confirmation.create_date = instance.create_date
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
        invoice.title = offer.title
        invoice.description = offer.description
        invoice.iban = offer.payment_information.iban
        invoice.bic_swift = offer.payment_information.bic_swift
        invoice.kontonummer = offer.payment_information.kontonummer
        invoice.bemerkung = offer.bemerkung
        # invoice.zahlbar_bis = offer.create_date + timedelta(days=30)
        invoice.netto_price = offer.get_netto_price()
        invoice.mwst = offer.get_mwst()
        invoice.invoice_amount_total = offer.get_invoice_amount_total()
        # invoice.create_date = offer.create_date
        invoice.category = offer.category
        invoice.save()

        offer_confirmation = OfferConfirmation.objects.get(offer=offer, number=offer.number)
        offer_confirmation.client_address = offer.client_address
        offer_confirmation.client_name = offer.client_name
        offer_confirmation.email = offer.email
        offer_confirmation.title = offer.title
        offer_confirmation.description = offer.description
        offer_confirmation.iban = offer.payment_information.iban
        offer_confirmation.bic_swift = offer.payment_information.bic_swift
        offer_confirmation.kontonummer = offer.payment_information.kontonummer
        offer_confirmation.bemerkung = offer.bemerkung
        # offer_confirmation.zahlbar_bis = offer.create_date + timedelta(days=30)
        offer_confirmation.netto_price = offer.get_netto_price()
        offer_confirmation.mwst = offer.get_mwst()
        offer_confirmation.invoice_amount_total = offer.get_invoice_amount_total()
        # offer_confirmation.create_date = offer.create_date
        offer_confirmation.category = offer.category
        offer_confirmation.save()
    except Exception as e:
        print(e)
