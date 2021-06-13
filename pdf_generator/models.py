import datetime

from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    create_date = models.DateTimeField(null=True, auto_now_add=True)
    write_date = models.DateTimeField(null=True, auto_now=True)


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


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class Template(BaseModel):
    number = models.IntegerField(primary_key=True)
    client_address = models.TextField(max_length=512, null=True)
    client_name = models.TextField(max_length=128, null=True)
    email = models.EmailField(null=True)
    description = models.TextField(max_length=512, null=True)
    signature = models.ForeignKey(to=Signature, null=True, related_name='templates', on_delete=models.SET_NULL)
    payment_information = models.ForeignKey(to=PaymentInformation, null=True, related_name='templates', on_delete=models.SET_NULL) # noqa
    category = models.ForeignKey(to=Category, null=True, related_name='templates', on_delete=models.SET_NULL)
    bemerkung = models.TextField(max_length=512, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    name = models.TextField(max_length=512, null=False, unique=True)

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
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class Offer(BaseModel):
    number = models.IntegerField(primary_key=True)
    client_address = models.TextField(max_length=512, null=True, blank=True)
    client_name = models.TextField(max_length=128, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    description = models.TextField(max_length=512, null=True, blank=True)
    signature = models.ForeignKey(to=Signature, null=True, blank=True, related_name='offers', on_delete=models.SET_NULL)
    payment_information = models.ForeignKey(to=PaymentInformation, null=True, blank=True, related_name='offers', on_delete=models.SET_NULL) # noqa
    category = models.ForeignKey(to=Category, null=True, blank=True, related_name='offers', on_delete=models.SET_NULL)
    bemerkung = models.TextField(max_length=512, null=True, blank=True)
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    template = models.ForeignKey(to=Template, null=True, blank=True, related_name='offers', on_delete=models.SET_NULL)
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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
                + str(datetime.datetime.now().minute)
            if len(self.number) == 8:
                self.number += '0'
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        super(self.__class__, self).save(*args, **kwargs)

    def get_netto_price(self):
        designations = Designation.objects.filter(
            phase__in=Phase.objects.filter(page__in=Page.objects.filter(offer=self.number))
        )

        self.netto_price = sum([designation.price * designation.quantity for designation in designations])
        self.netto_price = float('{:.1f}'.format(self.netto_price))
        return self.netto_price

    def get_mwst(self):
        self.mwst = (self.netto_price * 7.7)/100
        self.mwst = float('{:.1f}'.format(self.mwst))
        return self.mwst

    def get_invoice_amount_total(self):
        # self.invoice_amount_total = self.netto_price + self.mwst
        self.invoice_amount_total = self.get_netto_price() + self.get_mwst()
        self.invoice_amount_total = float('{:.1f}'.format(self.invoice_amount_total))
        return self.invoice_amount_total


class Page(BaseModel):
    offer = models.ForeignKey(to=Offer, related_name='pages', on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(null=False, blank=False, default=1)

    def __str__(self):
        return f'Page {self.number}'


class Phase(BaseModel):
    page = models.ForeignKey(to=Page, related_name='phases', on_delete=models.CASCADE)
    name = models.TextField(max_length=128, null=True, blank=True, default='phase')
    number = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Designation(BaseModel):
    phase = models.ForeignKey(to=Phase, related_name='designations', on_delete=models.CASCADE)
    name = models.TextField(max_length=512, null=True)
    description = models.TextField(max_length=512, null=True)
    price = models.FloatField(null=False, blank=False, default=0)
    quantity = models.PositiveSmallIntegerField(null=False, blank=False, default=1)
    number = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    def get_subtotal(self):
        self.subtotal = self.price * self.quantity
        return self.subtotal


class Invoice(BaseModel):
    offer = models.OneToOneField(to=Offer, related_name='invoice', on_delete=models.CASCADE)
    number = models.IntegerField(primary_key=True)
    client_address = models.TextField(max_length=512, null=True)
    client_name = models.TextField(max_length=128, null=True)
    email = models.EmailField(null=True)
    description = models.TextField(max_length=512, null=True)
    iban = models.TextField(max_length=32, default='CH26 0483 5216 7077 3100 0', null=True)
    bic_swift = models.TextField(max_length=32, default='CRESCHZZ80A', null=True)
    kontonummer = models.TextField(max_length=32, default='2167077-32', null=True)
    bemerkung = models.TextField(max_length=512, null=True, blank=True)
    zahlbar_bis = models.DateTimeField(null=True)
    netto_price = models.IntegerField(null=True)
    mwst = models.IntegerField(null=True)
    invoice_amount_total = models.IntegerField(null=True)
    sent = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    category = models.ForeignKey(to=Category, null=True, related_name='invoices', on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-create_date"]
        verbose_name = "Rechnung"
        verbose_name_plural = "Rechnugen"

    def __str__(self):
        return f'{self.number}'


class OfferConfirmation(BaseModel):
    offer = models.OneToOneField(to=Offer, related_name='offer_confirmation', on_delete=models.CASCADE)
    number = models.IntegerField(primary_key=True)
    client_address = models.TextField(max_length=512, null=True)
    client_name = models.TextField(max_length=128, null=True)
    email = models.EmailField(null=True)
    description = models.TextField(max_length=512, null=True)
    iban = models.TextField(max_length=32, default='CH26 0483 5216 7077 3100 0', null=True)
    bic_swift = models.TextField(max_length=32, default='CRESCHZZ80A', null=True)
    kontonummer = models.TextField(max_length=32, default='2167077-32', null=True)
    bemerkung = models.TextField(max_length=512, null=True, blank=True)
    zahlbar_bis = models.DateTimeField(null=True)
    netto_price = models.IntegerField(null=True)
    mwst = models.IntegerField(null=True)
    invoice_amount_total = models.IntegerField(null=True)
    sent = models.BooleanField(default=False)
    signed = models.BooleanField(default=False)
    signed_file = models.FileField(null=True)
    category = models.ForeignKey(to=Category, null=True, related_name='offer_confirmations', on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-create_date"]
        verbose_name = "Auftragsbestätigung"
        verbose_name_plural = "Auftragsbestätigungen"

    def __str__(self):
        return f'{self.number}'
