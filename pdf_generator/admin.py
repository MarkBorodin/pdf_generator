import math

import nested_admin
from django.contrib import admin
from django.forms import Textarea
from django.urls import reverse
from django.utils.safestring import mark_safe
from nested_admin.nested import NestedTabularInline

from .models import Category, Designation, Offer, Page, Phase, models, Invoice, \
    OfferConfirmation, Signature, PaymentInformation, Template, HourlyRate, GlobalTexts, InvoiceWithoutOffer


class DesignationInline(NestedTabularInline, nested_admin.NestedStackedInline): # noqa
    model = Designation
    fields = ('name', 'description', 'nach_aufwand', 'price', 'fixed_price', 'number_of_hours', 'quantity')
    show_change_link = True
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 55})},
    }


class PhaseInline(NestedTabularInline, nested_admin.NestedStackedInline):  # noqa
    model = Phase
    fields = ('name', 'hours_to_months')
    inlines = [DesignationInline]
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 170})},
    }


class PageInline(NestedTabularInline, nested_admin.NestedStackedInline):  # noqa
    model = Page
    inlines = [PhaseInline]
    extra = 0
    fields = ('number',)
    readonly_fields = ('offer', 'template', 'invoice_without_offer')


class OfferAdmin(nested_admin.NestedModelAdmin):  # noqa
    model = Offer
    save_as = True
    inlines = [PageInline]
    list_display = (
        'number', 'create_date', 'title', 'client_name', 'amount_total', 'category',
        'view_pdf_offer', 'get_pdf_offer', 'create_invoice', 'create_offer_confirmation'
    )
    search_fields = (
        'number', 'create_date', 'client_address', 'client_name', 'client_address', 'email', 'description',
        'category__name'
    )
    list_filter = ('create_date', 'category')
    fields = (
        'template', 'client_name', 'client_address', 'email', 'title', 'description', 'bemerkung', 'payment_information',
        'signature', 'category', 'global_texts'
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 170})},
        models.EmailField: {'widget': Textarea(attrs={'rows': 1, 'cols': 170})},
    }

    def get_readonly_fields(self, request, obj=None): # noqa
        if obj:
            return 'template'
        else:
            return []

    def amount_total(self, obj):  # noqa
        amount_total = obj.get_invoice_amount_total()
        return amount_total

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
        'number', 'zahlbar_bis', 'client_name', 'invoice_amount_total', 'category',
        'sent', 'paid', 'view_pdf_invoice', 'get_pdf_invoice'
    )
    search_fields = (
        'number', 'create_date', 'client_address', 'client_name', 'client_address', 'email', 'description',
        'sent', 'paid', 'category__name'
                     )
    list_filter = ('sent', 'paid', 'create_date', 'client_address', 'client_name', 'email', 'description', 'category')
    fields = (
        'sent', 'paid', 'client_address', 'client_name', 'email', 'title', 'description', 'iban', 'bic_swift',
        'kontonummer', 'bemerkung', 'create_date', 'zahlbar_bis', 'netto_price', 'mwst', 'invoice_amount_total', 'category',
        'global_texts'
    )
    list_editable = ('sent', 'paid',)

    change_list_template = 'admin/pdf_generator/invoice/change_list.html'

    @staticmethod
    def get_sum_open_sent_paid():
        sum_open_sent_paid = dict()
        invoices = Invoice.objects.all() # noqa
        invoices_without_offers = InvoiceWithoutOffer.objects.all() # noqa
        sum_open_invoices = sum([invoice.invoice_amount_total for invoice in invoices if not invoice.sent and not invoice.paid]) # noqa
        sum_sent_invoices = sum([invoice.invoice_amount_total for invoice in invoices if invoice.sent and not invoice.paid]) # noqa
        sum_paid_invoices = sum([invoice.invoice_amount_total for invoice in invoices if invoice.paid]) # noqa

        sum_open_without_offers = sum([invoice.get_invoice_amount_total() for invoice in invoices_without_offers if not invoice.sent and not invoice.paid])  # noqa
        sum_sent_without_offers = sum([invoice.get_invoice_amount_total() for invoice in invoices_without_offers if invoice.sent and not invoice.paid])  # noqa
        sum_paid_without_offers = sum([invoice.get_invoice_amount_total() for invoice in invoices_without_offers if invoice.paid])  # noqa

        sum_open_sent_paid['sum_open_invoices'] = float('{:.2f}'.format(sum_open_invoices + sum_open_without_offers))
        sum_open_sent_paid['sum_sent_invoices'] = float('{:.2f}'.format(sum_sent_invoices + sum_sent_without_offers))
        sum_open_sent_paid['sum_paid_invoices'] = float('{:.2f}'.format(sum_paid_invoices + sum_paid_without_offers))
        return sum_open_sent_paid

    def changelist_view(self, request, extra_context=None): # noqa
        sum_open_sent_paid = self.get_sum_open_sent_paid()
        my_context = {
            'open': sum_open_sent_paid['sum_open_invoices'],
            'sent': sum_open_sent_paid['sum_sent_invoices'],
            'paid': sum_open_sent_paid['sum_paid_invoices'],
        }
        return super(InvoiceAdmin, self).changelist_view(request, extra_context=my_context)

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


class InvoiceWithoutOfferAdmin(nested_admin.NestedModelAdmin):  # noqa
    inlines = [PageInline]
    model = InvoiceWithoutOffer
    list_display = (
        'number', 'zahlbar_bis', 'client_name', 'view_invoice_amount_total', 'category',
        'sent', 'paid',
        'view_pdf_invoice_without_offer', 'get_pdf_invoice_without_offer'
    )
    search_fields = (
        'number', 'create_date', 'client_address', 'client_name', 'client_address', 'email', 'description',
        'sent', 'paid', 'category__name'
                     )
    list_filter = ('sent', 'paid', 'create_date', 'client_address', 'client_name', 'email', 'description', 'category')
    fields = (
        'template', 'sent', 'paid', 'client_address', 'client_name', 'email', 'title', 'description', 'iban', 'bic_swift',
        'kontonummer', 'bemerkung', 'create_date', 'zahlbar_bis', 'netto_price', 'mwst', 'invoice_amount_total',
        'category', 'global_texts', 'signature', 'payment_information'
    )
    list_editable = ('sent', 'paid',)
    change_list_template = 'admin/pdf_generator/invoice/change_list.html'
    save_as = True

    def get_readonly_fields(self, request, obj=None): # noqa
        if obj:
            return 'template'
        else:
            return []

    @staticmethod
    def get_sum_open_sent_paid():
        sum_open_sent_paid = dict()
        invoices = Invoice.objects.all()  # noqa
        invoices_without_offers = InvoiceWithoutOffer.objects.all()  # noqa
        sum_open_invoices = sum([invoice.invoice_amount_total for invoice in invoices if not invoice.sent and not invoice.paid])  # noqa
        sum_sent_invoices = sum([invoice.invoice_amount_total for invoice in invoices if invoice.sent and not invoice.paid])  # noqa
        sum_paid_invoices = sum([invoice.invoice_amount_total for invoice in invoices if invoice.paid])  # noqa
        sum_open_without_offers = sum([invoice.get_invoice_amount_total() for invoice in invoices_without_offers if not invoice.sent and not invoice.paid])  # noqa
        sum_sent_without_offers = sum([invoice.get_invoice_amount_total() for invoice in invoices_without_offers if invoice.sent and not invoice.paid])  # noqa
        sum_paid_without_offers = sum([invoice.get_invoice_amount_total() for invoice in invoices_without_offers if invoice.paid])  # noqa

        sum_open_sent_paid['sum_open_invoices'] = float('{:.2f}'.format(sum_open_invoices + sum_open_without_offers))
        sum_open_sent_paid['sum_sent_invoices'] = float('{:.2f}'.format(sum_sent_invoices + sum_sent_without_offers))
        sum_open_sent_paid['sum_paid_invoices'] = float('{:.2f}'.format(sum_paid_invoices + sum_paid_without_offers))
        return sum_open_sent_paid

    def view_invoice_amount_total(self, obj):
        return obj.get_invoice_amount_total()

    def changelist_view(self, request, extra_context=None): # noqa
        sum_open_sent_paid = self.get_sum_open_sent_paid()
        my_context = {
            'open': sum_open_sent_paid['sum_open_invoices'],
            'sent': sum_open_sent_paid['sum_sent_invoices'],
            'paid': sum_open_sent_paid['sum_paid_invoices'],
        }
        return super(InvoiceWithoutOfferAdmin, self).changelist_view(request, extra_context=my_context)

    def view_pdf_invoice_without_offer(self, obj): # noqa
        return mark_safe(
            f'<a target="_blank" class="button"'
            f'href="{reverse("pdf_generator:view_pdf_invoice_without_offer", args=[obj.pk])}">View PDF invoice</a>'
        )

    def get_pdf_invoice_without_offer(self, obj): # noqa
        return mark_safe(
            f'<a target="_blank" class="button" style="background: green;"'
            f'href="{reverse("pdf_generator:get_pdf_invoice_without_offer", args=[obj.pk])}">Get PDF invoice</a>'
        )


class OfferConfirmationAdmin(nested_admin.NestedModelAdmin):  # noqa
    model = OfferConfirmation
    list_display = (
        'number', 'zahlbar_bis', 'client_name', 'invoice_amount_total', 'category',
        'sent', 'signed', 'view_pdf_offer_confirmation', 'get_pdf_offer_confirmation', 'view_signed_file',
    )
    search_fields = (
        'number', 'create_date', 'client_address', 'client_name', 'client_address', 'email', 'description',
        'sent', 'signed', 'category__name'
                     )
    list_filter = (
        'sent', 'signed', 'create_date', 'client_address', 'client_name', 'email', 'description', 'category'
    )
    fields = (
        'signed_file', 'sent', 'signed', 'client_address', 'client_name', 'email', 'title', 'description', 'iban',
        'bic_swift', 'kontonummer', 'bemerkung', 'zahlbar_bis', 'netto_price', 'mwst', 'invoice_amount_total',
        'category', 'global_texts'
    )
    list_editable = ('sent', 'signed')

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


class CategoryAdmin(nested_admin.NestedModelAdmin):  # noqa
    model = Category
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    fields = ('name',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 170})},
    }


class TemplateAdmin(nested_admin.NestedModelAdmin):  # noqa
    model = Template
    inlines = [PageInline]
    list_display = (
        'name', 'number', 'create_date', 'client_name', 'category', 'global_texts'
    )
    search_fields = (
        'number', 'create_date', 'client_address', 'client_name', 'client_address', 'email', 'description',
        'category__name'
    )
    list_filter = ('create_date', 'client_address', 'client_name', 'email', 'description', 'category')
    fields = (
        'name', 'client_name', 'client_address', 'email', 'description', 'bemerkung', 'payment_information',
        'signature', 'category', 'global_texts'
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 170})},
        models.EmailField: {'widget': Textarea(attrs={'rows': 1, 'cols': 170})},
    }


class GlobalTextsAdmin(nested_admin.NestedModelAdmin):  # noqa
    model = GlobalTexts
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    fields = ('name', 'bottom_text', 'url')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 170})},
    }


class HourlyRateAdmin(nested_admin.NestedModelAdmin):  # noqa
    model = HourlyRate
    list_display = ('rate', 'name')
    search_fields = ('name', 'rate')
    list_filter = ('name', 'rate')
    fields = ('rate', 'name')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 170})},
    }


admin.site.register(Category, CategoryAdmin)
admin.site.register(PaymentInformation, PaymentInformationAdmin)
admin.site.register(Signature, SignatureAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceWithoutOffer, InvoiceWithoutOfferAdmin)
admin.site.register(OfferConfirmation, OfferConfirmationAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(GlobalTexts, GlobalTextsAdmin)
admin.site.register(HourlyRate, HourlyRateAdmin)
