import nested_admin
from django.contrib import admin
from django.forms import Textarea
from django.urls import reverse
from django.utils.safestring import mark_safe
from nested_admin.nested import NestedTabularInline

from .models import Designation, Offer, Page, Phase, models, Invoice, OfferConfirmation, Signature, PaymentInformation


class DesignationInline(NestedTabularInline, nested_admin.NestedStackedInline): # noqa
    model = Designation
    fields = ('name', 'description', 'price', 'quantity')
    show_change_link = True
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 70})},
    }


class PhaseInline(NestedTabularInline, nested_admin.NestedStackedInline):  # noqa
    model = Phase
    fields = ('name',)
    inlines = [DesignationInline]
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 170})},
    }


class PageInline(NestedTabularInline, nested_admin.NestedStackedInline):  # noqa
    model = Page
    inlines = [PhaseInline]
    extra = 0


class OfferAdmin(nested_admin.NestedModelAdmin):  # noqa
    model = Offer
    inlines = [PageInline]
    list_display = (
        'number', 'create_date', 'client_name', 'client_address', 'email',
        'view_pdf_offer', 'get_pdf_offer', 'create_invoice', 'create_offer_confirmation'
    )
    search_fields = ('number', 'create_date', 'client_address', 'client_name', 'client_address', 'email', 'description')
    list_filter = ('create_date', 'client_address', 'client_name', 'email', 'description')
    fields = (
        'client_address', 'client_name', 'email', 'description', 'bemerkung', 'payment_information',
        'signature',
    )
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

    def create_offer_confirmation(self, obj): # noqa
        return mark_safe(
            f'<a target="_blank" class="button" style="background: orange;"'
            f'href="{reverse("pdf_generator:create_offer_confirmation", args=[obj.pk])}">Create offer confirmation</a>'
        )


class InvoiceAdmin(nested_admin.NestedModelAdmin):  # noqa
    model = Invoice
    list_display = (
        'number', 'zahlbar_bis', 'client_name', 'client_address', 'email', 'send', 'paid', 'view_pdf_invoice',
        'get_pdf_invoice'
    )
    search_fields = (
        'number', 'create_date', 'client_address', 'client_name', 'client_address', 'email', 'description',
        'send', 'paid',
                     )
    list_filter = ('send', 'paid', 'create_date', 'client_address', 'client_name', 'email', 'description')
    fields = (
        'send', 'paid', 'client_address', 'client_name', 'email', 'description', 'iban', 'bic_swift', 'kontonummer',
        'bemerkung', 'zahlbar_bis', 'netto_price', 'mwst', 'invoice_amount_total'
    )
    list_editable = ('send', 'paid',)

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


class OfferConfirmationAdmin(nested_admin.NestedModelAdmin):  # noqa
    model = OfferConfirmation
    list_display = (
        'number', 'zahlbar_bis', 'client_name', 'client_address', 'email', 'send', 'signed',
        'view_pdf_offer_confirmation', 'get_pdf_offer_confirmation', 'view_signed_file',
    )
    search_fields = (
        'number', 'create_date', 'client_address', 'client_name', 'client_address', 'email', 'description',
        'send', 'signed',
                     )
    list_filter = (
        'send', 'signed', 'create_date', 'client_address', 'client_name', 'email', 'description'
    )
    fields = (
        'signed_file', 'send', 'signed', 'client_address', 'client_name', 'email', 'description', 'iban', 'bic_swift',
        'kontonummer', 'bemerkung', 'zahlbar_bis', 'netto_price', 'mwst', 'invoice_amount_total'
    )
    list_editable = ('send', 'signed')

    def view_pdf_offer_confirmation(self, obj): # noqa
        return mark_safe(
            f'<a target="_blank" class="button" '
            f'href="{reverse("pdf_generator:view_pdf_confirmation", args=[obj.pk])}">'
            f'View PDF offer confirmation</a>'
        )

    def get_pdf_offer_confirmation(self, obj):  # noqa
        return mark_safe(
            f'<a target="_blank" class="button" style="background: green;"'
            f'href="{reverse("pdf_generator:get_pdf_confirmation", args=[obj.pk])}">'
            f'Get PDF offer confirmation</a>'
        )

    def view_signed_file(self, obj):  # noqa
        offer_confirmation = OfferConfirmation.objects.get(number=obj.pk)  # noqa
        file = offer_confirmation.signed_file
        if file != None: # noqa
            return mark_safe(
                f'<a target="_blank" class="button" style="background: purple;"'
                f'href="{reverse("pdf_generator:view_signed_file", args=[obj.pk])}">'
                f'Signed file</a>'
            )


class SignatureAdmin(nested_admin.NestedModelAdmin):  # noqa
    model = Signature
    list_display = (
        'id', 'image', 'name',
    )
    search_fields = ('id', 'image', 'name', )
    list_filter = ('id', 'image', 'name', )
    fields = ('image', 'name', )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 170})},
    }


class PaymentInformationAdmin(nested_admin.NestedModelAdmin):  # noqa
    model = Signature
    list_display = (
        'currency', 'iban', 'bic_swift', 'kontonummer',
    )
    search_fields = ('currency', 'iban', 'bic_swift', 'kontonummer',)
    list_filter = ('currency', 'iban', 'bic_swift', 'kontonummer',)
    fields = ('currency', 'iban', 'bic_swift', 'kontonummer',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 170})},
    }


admin.site.register(PaymentInformation, PaymentInformationAdmin)
admin.site.register(Signature, SignatureAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(OfferConfirmation, OfferConfirmationAdmin)
