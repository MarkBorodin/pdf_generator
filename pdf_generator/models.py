from datetime import timedelta

import datetime

from django.db import models
from django.utils import timezone


SCHLUSSTEXT = """Wir bedanken uns für den Auftrag und freuen uns auf eine erfolgreiche Zusammenarbeit. 
Bitte senden Sie dieses Dokument gegengezeichnet an uns uruck."""
BOTTOM_TEXT = """Es gelten die Allgemeinen Geschäftsbedingungen der Marketing Monkeys. Diese findest du unter: """
URL = """https://www.marketingmonkeys.ch/agb/"""


class BaseModel(models.Model):
    class Meta:
        abstract = True
    # test = models.TextField()
    create_date = models.DateTimeField(null=True, default=timezone.now, editable=True)
    # create_date = models.DateField(null=True, blank=True, default=datetime.date.today, editable=True)
    write_date = models.DateTimeField(null=True, auto_now=True, editable=True)
    # write_date = models.DateField(null=True, blank=True, default=datetime.date.today, editable=True)


class GlobalTexts(BaseModel):
    name = models.CharField(max_length=128, null=False, blank=False)
    bottom_text = models.TextField(max_length=256, null=True, blank=True, default=BOTTOM_TEXT)
    url = models.TextField(max_length=128, null=True, blank=True, default=URL)

    class Meta:
        ordering = ["-create_date"]
        verbose_name = "Globaler Text"
        verbose_name_plural = "Globale Texte"

    def __str__(self):
        return self.name


class HourlyRate(BaseModel):
    rate = models.FloatField(default=30, null=True)
    name = models.TextField(max_length=256, null=True, blank=True)

    class Meta:
        ordering = ["-create_date"]
        verbose_name = "hourly rate"
        verbose_name_plural = "hourly rate"

    def __str__(self):
        return f'{self.name} {self.rate}'


class Signature(BaseModel):
    image = models.ImageField()
    image_code = models.TextField(null=True)
    name = models.TextField(null=False)

    class Meta:
        ordering = ["-create_date"]
        verbose_name = "Signatur"
        verbose_name_plural = "Signaturen"

    def __str__(self):
        return f'{self.name}'


class PaymentInformation(BaseModel):
    currency = models.TextField(max_length=32, default='CHF', null=True)
    iban = models.TextField(max_length=32, default='CH26 0483 5216 7077 3100 0', null=True)
    bic_swift = models.TextField(max_length=32, default='CRESCHZZ80A', null=True)
    kontonummer = models.TextField(max_length=32, default='2167077-32', null=True)

    class Meta:
        ordering = ["-create_date"]
        verbose_name = "Zahlungsinformation"
        verbose_name_plural = "Zahlungsinformationen"

    def __str__(self):
        return f'{self.currency}'


class Category(BaseModel):
    name = models.TextField(max_length=128, null=False)

    class Meta:
        ordering = ["-create_date"]
        verbose_name = "Kategorie"
        verbose_name_plural = "Kategorien"

    def __str__(self):
        return f'{self.name}'


class Template(BaseModel):
    number = models.IntegerField(primary_key=True)
    client_address = models.TextField(max_length=512, null=True)
    client_name = models.TextField(max_length=128, null=True)
    email = models.EmailField(null=True)
    description = models.TextField(max_length=512, null=True, blank=True)
    signature = models.ForeignKey(to=Signature, null=True, related_name='templates', on_delete=models.SET_NULL)
    payment_information = models.ForeignKey(to=PaymentInformation, null=True, related_name='templates', on_delete=models.SET_NULL) # noqa
    category = models.ForeignKey(to=Category, null=True, related_name='templates', on_delete=models.SET_NULL)
    bemerkung = models.TextField(max_length=512, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    name = models.TextField(max_length=512, null=False, unique=True)
    global_texts = models.ForeignKey(to=GlobalTexts, null=True, blank=True, related_name='templates', on_delete=models.SET_NULL) # noqa

    class Meta:
        ordering = ["-create_date"]
        verbose_name = "Vorlage"
        verbose_name_plural = "Vorlagen"

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if self.number is None:
            self.number = \
                str(datetime.datetime.now().year)\
                + str(datetime.datetime.now().month)\
                + str(datetime.datetime.now().hour)\
                + str(datetime.datetime.now().minute)
            if len(self.number) == 8:
                self.number += '0'
        super(self.__class__, self).save(*args, **kwargs)


class Offer(BaseModel):
    number = models.IntegerField(primary_key=True)
    client_address = models.TextField(max_length=512, null=True, blank=True)
    client_name = models.TextField(max_length=128, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    title = models.TextField(max_length=256, null=True, blank=True)
    description = models.TextField(max_length=512, null=True, blank=True)
    signature = models.ForeignKey(to=Signature, null=True, blank=True, related_name='offers', on_delete=models.SET_NULL)
    payment_information = models.ForeignKey(to=PaymentInformation, null=True, blank=True, related_name='offers', on_delete=models.SET_NULL) # noqa
    global_texts = models.ForeignKey(to=GlobalTexts, null=True, blank=True, related_name='offers', on_delete=models.SET_NULL) # noqa
    category = models.ForeignKey(to=Category, null=True, blank=True, related_name='offers', on_delete=models.SET_NULL)
    bemerkung = models.TextField(max_length=512, null=True, blank=True)
    template = models.ForeignKey(to=Template, null=True, blank=True, related_name='offers', on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-create_date"]
        verbose_name = "Offerte"
        verbose_name_plural = "Offerten"

    def __str__(self):
        return f'{self.number}'

    def save(self, *args, **kwargs):
        if self.number is None:
            self.number = \
                str(datetime.datetime.now().year)\
                + str(datetime.datetime.now().month)\
                + str(datetime.datetime.now().hour)\
                + str(datetime.datetime.now().minute) \
                + str(datetime.datetime.now().second)
            if len(self.number) > 9:
                self.number = self.number[2:]
                if len(self.number) == 8:
                    self.number = self.number + '0'
        if self.template is not None:
            template = Template.objects.get(name=self.template.name)
            self.client_address = template.client_address
            self.client_name = template.client_name
            self.email = template.email
            self.description = template.description
            self.signature = template.signature
            self.payment_information = template.payment_information
            self.category = template.category
            self.bemerkung = template.bemerkung
            self.global_texts = template.global_texts

            pages = Page.objects.filter(template=template.number)

            for page in pages:
                page_new = Page.objects.create(
                    offer=self,
                    number=page.number
                )
                page_new.save()
                phases = Phase.objects.filter(page=page.id)

                for phase in phases:
                    phase_new = Phase.objects.create(
                        page=page_new,
                        name=phase.name,
                        number=phase.number
                    )
                    phase_new.save()
                    designations = Designation.objects.filter(phase=phase.id)

                    for designation in designations:
                        designation_new = Designation.objects.create(
                            phase=phase_new,
                            name=designation.name,
                            description=designation.description,
                            price=designation.price,
                            quantity=designation.quantity,
                            number_of_hours=designation.number_of_hours,
                            number=designation.number,
                            nach_aufwand=designation.nach_aufwand,
                            fixed_price=designation.fixed_price
                        )
                        designation_new.save()

        self.template = None
        super(self.__class__, self).save(*args, **kwargs)

    def get_netto_price(self):
        designations = Designation.objects.filter(
            phase__in=Phase.objects.filter(page__in=Page.objects.filter(offer=self.number))
        )
        self.netto_price = sum([designation.get_subtotal() for designation in designations]) # noqa
        self.netto_price = float('{:.2f}'.format(self.netto_price))
        return self.netto_price

    def get_mwst(self):
        self.mwst = (self.get_netto_price() * 7.7)/100
        self.mwst = float('{:.2f}'.format(self.mwst))
        return self.mwst

    def get_invoice_amount_total(self):
        self.invoice_amount_total = self.get_netto_price() + self.get_mwst()
        self.invoice_amount_total = float('{:.2f}'.format(self.invoice_amount_total))
        return self.invoice_amount_total


class Invoice(BaseModel):
    offer = models.OneToOneField(to=Offer, related_name='invoice', on_delete=models.CASCADE, null=True)
    number = models.IntegerField(primary_key=True)
    client_address = models.TextField(max_length=512, null=True)
    client_name = models.TextField(max_length=128, null=True)
    email = models.EmailField(null=True)
    title = models.TextField(max_length=256, null=True, blank=True)
    description = models.TextField(max_length=512, null=True, blank=True)
    iban = models.TextField(max_length=32, default='CH26 0483 5216 7077 3100 0', null=True)
    bic_swift = models.TextField(max_length=32, default='CRESCHZZ80A', null=True)
    kontonummer = models.TextField(max_length=32, default='2167077-32', null=True)
    bemerkung = models.TextField(max_length=512, null=True, blank=True)
    zahlbar_bis = models.DateTimeField(null=True)
    netto_price = models.IntegerField(null=True)
    mwst = models.IntegerField(null=True)
    invoice_amount_total = models.FloatField(null=True)
    sent = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    category = models.ForeignKey(to=Category, null=True, related_name='invoices', on_delete=models.SET_NULL)
    global_texts = models.ForeignKey(to=GlobalTexts, null=True, blank=True, related_name='invoices', on_delete=models.SET_NULL)  # noqa

    class Meta:
        ordering = ["-create_date"]
        verbose_name = "Rechnung"
        verbose_name_plural = "Rechnungen"

    def __str__(self):
        return f'{self.number}'


class InvoiceWithoutOffer(BaseModel):
    number = models.IntegerField(primary_key=True)
    client_address = models.TextField(max_length=512, null=True, blank=True)
    client_name = models.TextField(max_length=128, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    title = models.TextField(max_length=256, null=True, blank=True)
    description = models.TextField(max_length=512, null=True, blank=True)
    iban = models.TextField(max_length=32, default='CH26 0483 5216 7077 3100 0', null=True, blank=True)
    bic_swift = models.TextField(max_length=32, default='CRESCHZZ80A', null=True, blank=True)
    kontonummer = models.TextField(max_length=32, default='2167077-32', null=True, blank=True)
    bemerkung = models.TextField(max_length=512, null=True, blank=True)
    zahlbar_bis = models.DateTimeField(null=True, blank=True)
    netto_price = models.IntegerField(null=True, blank=True)
    mwst = models.IntegerField(null=True, blank=True)
    invoice_amount_total = models.FloatField(null=True, blank=True)
    sent = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    category = models.ForeignKey(to=Category, null=True, blank=True, related_name='invoices_without_offer', on_delete=models.SET_NULL)   # noqa
    global_texts = models.ForeignKey(to=GlobalTexts, null=True, blank=True, related_name='invoices_without_offer', on_delete=models.SET_NULL)  # noqa
    signature = models.ForeignKey(to=Signature, null=True, blank=True, related_name='invoices_without_offer', on_delete=models.SET_NULL)    # noqa
    payment_information = models.ForeignKey(to=PaymentInformation, null=True, blank=True, related_name='invoices_without_offer', on_delete=models.SET_NULL) # noqa
    template = models.ForeignKey(to=Template, null=True, blank=True, related_name='invoices_without_offer', on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-create_date"]
        verbose_name = "Rechnung ohne Offerte"
        verbose_name_plural = "Rechnungen ohne Offerten"

    def save(self, *args, **kwargs):
        if self.number is None:
            self.number = \
                str(datetime.datetime.now().year)\
                + str(datetime.datetime.now().month)\
                + str(datetime.datetime.now().hour)\
                + str(datetime.datetime.now().minute) \
                + str(datetime.datetime.now().second)
            if len(self.number) > 9:
                self.number = self.number[2:]
                if len(self.number) == 8:
                    self.number = self.number + '0'
            self.zahlbar_bis = self.create_date + timedelta(days=30)

        if self.template is not None:
            template = Template.objects.get(name=self.template.name)
            self.client_address = template.client_address
            self.client_name = template.client_name
            self.email = template.email
            self.description = template.description
            self.signature = template.signature
            self.payment_information = template.payment_information
            self.category = template.category
            self.bemerkung = template.bemerkung
            self.global_texts = template.global_texts

            pages = Page.objects.filter(template=template.number)

            for page in pages:
                page_new = Page.objects.create(
                    invoice_without_offer=self,
                    number=page.number
                )
                page_new.save()
                phases = Phase.objects.filter(page=page.id)

                for phase in phases:
                    phase_new = Phase.objects.create(
                        page=page_new,
                        name=phase.name,
                        number=phase.number
                    )
                    phase_new.save()
                    designations = Designation.objects.filter(phase=phase.id)

                    for designation in designations:
                        designation_new = Designation.objects.create(
                            phase=phase_new,
                            name=designation.name,
                            description=designation.description,
                            price=designation.price,
                            quantity=designation.quantity,
                            number_of_hours=designation.number_of_hours,
                            number=designation.number,
                            nach_aufwand=designation.nach_aufwand,
                            fixed_price=designation.fixed_price
                        )
                        designation_new.save()

        self.template = None
        super(self.__class__, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.number}'

    def get_netto_price(self):
        designations = Designation.objects.filter(
            phase__in=Phase.objects.filter(page__in=Page.objects.filter(invoice_without_offer=self.number))
        )
        self.netto_price = sum([designation.get_subtotal() for designation in designations]) # noqa
        self.netto_price = float('{:.2f}'.format(self.netto_price))
        return self.netto_price

    def get_mwst(self):
        self.mwst = (self.get_netto_price() * 7.7)/100
        self.mwst = float('{:.2f}'.format(self.mwst))
        return self.mwst

    def get_invoice_amount_total(self):
        self.invoice_amount_total = self.get_netto_price() + self.get_mwst()
        self.invoice_amount_total = float('{:.2f}'.format(self.invoice_amount_total))
        return self.invoice_amount_total


class OfferConfirmation(BaseModel):
    offer = models.OneToOneField(to=Offer, related_name='offer_confirmation', on_delete=models.CASCADE)
    number = models.IntegerField(primary_key=True)
    client_address = models.TextField(max_length=512, null=True)
    client_name = models.TextField(max_length=128, null=True)
    email = models.EmailField(null=True)
    title = models.TextField(max_length=256, null=True, blank=True)
    description = models.TextField(max_length=512, null=True, blank=True)
    iban = models.TextField(max_length=32, default='CH26 0483 5216 7077 3100 0', null=True)
    bic_swift = models.TextField(max_length=32, default='CRESCHZZ80A', null=True)
    kontonummer = models.TextField(max_length=32, default='2167077-32', null=True)
    bemerkung = models.TextField(max_length=512, null=True, blank=True)
    zahlbar_bis = models.DateTimeField(null=True)
    netto_price = models.IntegerField(null=True)
    mwst = models.IntegerField(null=True)
    invoice_amount_total = models.FloatField(null=True)
    sent = models.BooleanField(default=False)
    signed = models.BooleanField(default=False)
    signed_file = models.FileField(null=True)
    category = models.ForeignKey(to=Category, null=True, related_name='offer_confirmations', on_delete=models.SET_NULL)
    schlusstext = models.TextField(max_length=512, null=True, blank=True, default=SCHLUSSTEXT)   # noqa TODO should be deleted
    global_texts = models.ForeignKey(to=GlobalTexts, null=True, blank=True, related_name='offer_confirmations', on_delete=models.SET_NULL)  # noqa

    class Meta:
        ordering = ["-create_date"]
        verbose_name = "Auftragsbestätigung"
        verbose_name_plural = "Auftragsbestätigungen"

    def __str__(self):
        return f'{self.number}'


class Page(BaseModel):
    offer = models.ForeignKey(to=Offer, related_name='pages', on_delete=models.CASCADE, null=True, blank=True)
    template = models.ForeignKey(to=Template, related_name='pages', on_delete=models.CASCADE, null=True, blank=True)
    invoice_without_offer = models.ForeignKey(to=InvoiceWithoutOffer, related_name='pages', on_delete=models.CASCADE, null=True, blank=True)  # noqa
    number = models.PositiveSmallIntegerField(null=False, blank=False, default=1)

    def __str__(self):
        return f'Page {self.number}'


class Phase(BaseModel):
    page = models.ForeignKey(to=Page, related_name='phases', on_delete=models.CASCADE)
    name = models.TextField(max_length=128, null=True, blank=True, default='phase')
    number = models.PositiveSmallIntegerField(null=True, blank=True)
    hours_to_months = models.BooleanField(default=False, verbose_name='hours to months?')
    main = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        super(Phase, self).__init__(*args, **kwargs)
        self._disable_signals = False

    def save(self, *args, **kwargs):
        if self._state.adding is True:

            # if this is the offer
            if self.page.offer:
                phases = Phase.objects.filter(page__in=Page.objects.filter(offer=self.page.offer), name=self.name)
            # if this is the invoice without offer
            elif self.page.invoice_without_offer:
                phases = Phase.objects.filter(page__in=Page.objects.filter(invoice_without_offer=self.page.invoice_without_offer), name=self.name)
            # if this is the template
            elif self.page.template:
                phases = Phase.objects.filter(page__in=Page.objects.filter(template=self.page.template), name=self.name)
            unique_phase = False if phases.count() > 0 else True
            if not unique_phase:
                self.number = phases[0].number
                self.main = False
            else:
                # if this is the offer
                if self.page.offer:
                    self.number = Phase.objects.filter(page__in=Page.objects.filter(offer=self.page.offer), main=True).count() + 1
                # if this is the invoice without offer
                elif self.page.invoice_without_offer:
                    self.number = Phase.objects.filter(page__in=Page.objects.filter(invoice_without_offer=self.page.invoice_without_offer), main=True).count() + 1
                # if this is the template
                elif self.page.template:
                    self.number = Phase.objects.filter(page__in=Page.objects.filter(template=self.page.template), main=True).count() + 1

        super(self.__class__, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    def for_loop_counter(self):
        designations = Designation.objects.filter(phase=self)
        designations_count = len(designations)
        phases_on_page = len(self.page.phases.all())
        if designations_count >= 3 and self.page.number == 1 and phases_on_page < 2:
            if designations_count >= 7:
                return 7
            elif designations_count < 7:
                return 5
        if designations_count > 4 and self.page.number == 1 and phases_on_page >= 2 and self == self.page.phases.all().first():
            return 6
        if phases_on_page > 1:
            if self == self.page.phases.all()[1] and self.page.number == 1 and phases_on_page >= 2:
                return 11

    def big_first_phase(self):
        phases = self.page.phases.all()
        big_first_phase = False
        if phases:
            big_first_phase = True if len(phases[0].designations.all()) > 4 else False
        if len(phases) > 1 and big_first_phase:
            return big_first_phase


class Designation(BaseModel):
    phase = models.ForeignKey(to=Phase, related_name='designations', on_delete=models.CASCADE)
    name = models.TextField(max_length=512, null=True)
    description = models.TextField(max_length=256, null=True, blank=True)
    price = models.ForeignKey(to=HourlyRate, related_name='designations', on_delete=models.SET_DEFAULT, default=HourlyRate.objects.all().first().pk, null=True, blank=True) # noqa
    # price = models.IntegerField(null=True, blank=True) # noqa
    quantity = models.SmallIntegerField(null=False, blank=False, default=1)
    number_of_hours = models.FloatField(null=False, blank=False, default=0)
    number = models.PositiveSmallIntegerField(null=True, blank=True)
    nach_aufwand = models.BooleanField(default=False)
    fixed_price = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

    def get_default_hourly_rate(self):
        return HourlyRate.objects.all().first()

    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = HourlyRate.objects.all().last()

        if self._state.adding is True:
            super(self.__class__, self).save(*args, **kwargs)
            current_phase = self.phase
            if current_phase.page.offer:
                # if this is the offer
                phases = Phase.objects.filter(page__in=Page.objects.filter(offer=current_phase.page.offer), name=current_phase.name)
            elif current_phase.page.invoice_without_offer:
                # if this is the invoice without offer
                phases = Phase.objects.filter(page__in=Page.objects.filter(invoice_without_offer=current_phase.page.invoice_without_offer), name=current_phase.name)
            elif current_phase.page.template:
                # if this is the template
                phases = Phase.objects.filter(page__in=Page.objects.filter(template=current_phase.page.template), name=current_phase.name)
            counter = 1
            for phase in phases:
                for designation in phase.designations.all():
                    designation.number = counter
                    counter = counter + 1
                    designation.save(update_fields=['number'])
        else:
            super(self.__class__, self).save(*args, **kwargs)

    def get_subtotal(self):
        if not self.fixed_price:
            self.subtotal = self.price.rate * (self.quantity * self.number_of_hours)
        else:
            self.subtotal = self.quantity
        return self.subtotal
