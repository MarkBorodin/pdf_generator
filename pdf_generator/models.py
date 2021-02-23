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
        designations = Designation.objects.filter(offer=self.number)
        self.netto_price = sum([designation.price * designation.quantity for designation in designations])
        return self.netto_price

    def get_mwst(self):
        self.mwst = (self.netto_price * 7.7)/100
        return self.mwst

    def get_invoice_amount_total(self):
        self.invoice_amount_total = self.netto_price + self.mwst
        return self.invoice_amount_total


class Designation(BaseModel):
    offer = models.ForeignKey(to=Offer, related_name='designations', on_delete=models.CASCADE, null=False, blank=False)
    name = models.TextField(max_length=512, null=True)
    description = models.TextField(max_length=512, null=True)
    price = models.FloatField(null=False, blank=False, default=0)
    quantity = models.PositiveSmallIntegerField(null=False, blank=False, default=1)

    def __str__(self):
        return f'{self.description}'

    def get_subtotal(self):
        self.subtotal = self.price * self.quantity
        return self.subtotal
