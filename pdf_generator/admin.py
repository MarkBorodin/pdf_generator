from django.contrib import admin
from django.forms import Textarea
from django.urls import reverse
from django.utils.safestring import mark_safe

import nested_admin
from nested_admin.nested import NestedTabularInline

from .models import Designation, Offer, Page, Phase, models, Invoice


class DesignationInline(NestedTabularInline, nested_admin.NestedStackedInline):
    model = Designation
    fields = ('name', 'description', 'price', 'quantity')
    show_change_link = True
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 70})},
    }


class PhaseInline(NestedTabularInline, nested_admin.NestedStackedInline):
    model = Phase
    fields = ('name',)
    inlines = [DesignationInline]
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 170})},
    }


class PageInline(NestedTabularInline, nested_admin.NestedStackedInline):
    model = Page
    inlines = [PhaseInline]
    extra = 0


class OfferAdmin(nested_admin.NestedModelAdmin):
    model = Offer
    inlines = [PageInline]
    list_display = (
        'number', 'create_date', 'client_name', 'client_address',
        'email', 'view_pdf_offer', 'get_pdf_offer', 'create_invoice',
    )
    search_fields = ('number', 'create_date', 'client_address', 'client_name', 'client_address', 'email', 'description')
    list_filter = ('number', 'create_date', 'client_address', 'client_name', 'email', 'description')
    fields = ('client_address', 'client_name', 'email', 'description', 'bemerkung', 'iban', 'bic_swift', 'kontonummer')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 170})},
        models.EmailField: {'widget': Textarea(attrs={'rows': 1, 'cols': 170})},
    }

    def get_pdf_offer(self, obj): # noqa
        return mark_safe(
            f'<a class="button" style="background: green;" '
            f'href="{reverse("pdf_generator:get_pdf_offer", args=[obj.pk])}">Get PDF offer</a>'
        )

    def view_pdf_offer(self, obj): # noqa
        return mark_safe(
            f'<a target="_blank" class="button" '
            f'href="{reverse("pdf_generator:view_pdf_offer", args=[obj.pk])}">View PDF offer</a>'
        )

    def create_invoice(self, obj): # noqa
        return mark_safe(
            f'<a target="_blank" class="button" style="background: purple;"'
            f'href="{reverse("pdf_generator:create_invoice", args=[obj.pk])}">Create invoice</a>'
        )


class InvoiceAdmin(nested_admin.NestedModelAdmin):
    model = Invoice
    list_display = (
        'number', 'zahlbar_bis', 'client_name', 'client_address', 'email', 'send', 'paid', 'view_pdf_invoice',
        'get_pdf_invoice'
    )
    search_fields = (
        'number', 'create_date', 'client_address', 'client_name', 'client_address', 'email', 'description',
        'send', 'paid',
                     )
    list_filter = ('send', 'paid', 'number', 'create_date', 'client_address', 'client_name', 'email', 'description')
    fields = (
        'send', 'paid', 'client_address', 'client_name', 'email', 'description', 'iban', 'bic_swift', 'kontonummer',
        'bemerkung', 'zahlbar_bis', 'netto_price', 'mwst', 'invoice_amount_total'
    )

    def get_pdf_invoice(self, obj):  # noqa
        return mark_safe(
            f'<a target="_blank" class="button" style="background: green;"'
            f'href="{reverse("pdf_generator:get_pdf_invoice", args=[obj.pk])}">Get PDF invoice</a>'
        )

    def view_pdf_invoice(self, obj): # noqa
        return mark_safe(
            f'<a target="_blank" class="button" '
            f'href="{reverse("pdf_generator:view_pdf_invoice", args=[obj.pk])}">View PDF invoice</a>'
        )


admin.site.register(Offer, OfferAdmin)
admin.site.register(Invoice, InvoiceAdmin)
