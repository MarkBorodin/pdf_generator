import datetime

from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    create_date = models.DateTimeField(null=True, auto_now_add=True)
    write_date = models.DateTimeField(null=True, auto_now=True)


class Offer(BaseModel):
    number = models.IntegerField(primary_key=True)
    client_address = models.TextField(max_length=512, null=True)
    client_name = models.TextField(max_length=128, null=True)
    email = models.EmailField(null=True)
    description = models.TextField(max_length=512, null=True)
    iban = models.TextField(max_length=32, default='CH26 0483 5216 7077 3100 0', null=True)
    bic_swift = models.TextField(max_length=32, default='CRESCHZZ80A', null=True)
    kontonummer = models.TextField(max_length=32, default='2167077-32', null=True)
    bemerkung = models.TextField(max_length=512, null=True, blank=True)

    class Meta:
        ordering = ["-create_date"]

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
        self.invoice_amount_total = self.netto_price + self.mwst
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

    def __str__(self):
        return f'{self.name}'


class Designation(BaseModel):
    phase = models.ForeignKey(to=Phase, related_name='designations', on_delete=models.CASCADE)
    name = models.TextField(max_length=512, null=True)
    description = models.TextField(max_length=512, null=True)
    price = models.FloatField(null=False, blank=False, default=0)
    quantity = models.PositiveSmallIntegerField(null=False, blank=False, default=1)

    def __str__(self):
        return f'{self.name}'

    def get_subtotal(self):
        self.subtotal = self.price * self.quantity
        return self.subtotal
