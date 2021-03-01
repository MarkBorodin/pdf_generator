from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.urls import reverse
from django.utils.safestring import mark_safe


from pdf_generator.forms import DesignationInlineFormSet
from pdf_generator.models import Designation, Offer


class DesignationsInline(admin.TabularInline):
    model = Designation
    fields = ('name', 'description', 'price', 'quantity')
    show_change_link = True
    extra = 0
    formset = DesignationInlineFormSet
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 70})},
    }


class OfferAdmin(admin.ModelAdmin):
    inlines = (DesignationsInline,)
    list_display = (
        'number', 'create_date', 'client_name', 'client_address', 'email', 'view_pdf_offer',
        'get_pdf_offer', 'view_pdf_invoice', 'get_pdf_invoice'
    )
    search_fields = ('number', 'create_date', 'client_address', 'client_name', 'client_address', 'email', 'description')
    list_filter = ('number', 'create_date', 'client_address', 'client_name', 'email', 'description')
    fields = ('client_address', 'client_name', 'email', 'description', 'iban', 'bic_swift', 'kontonummer')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 170})},
        models.EmailField: {'widget': Textarea(attrs={'rows': 1, 'cols': 170})},
    }

    def get_pdf_offer(self, obj): # noqa
        return mark_safe(
            f'<a class="button" href="{reverse("pdf_generator:get_pdf_offer", args=[obj.pk])}">Get PDF offer</a>'
        )

    def view_pdf_offer(self, obj): # noqa
        return mark_safe(
            f'<a target="_blank" class="button" '
            f'href="{reverse("pdf_generator:view_pdf_offer", args=[obj.pk])}">View PDF offer</a>'
        )

    def get_pdf_invoice(self, obj):  # noqa
        return mark_safe(
            f'<a target="_blank" class="button" '
            f'href="{reverse("pdf_generator:get_pdf_invoice", args=[obj.pk])}">Get PDF invoice</a>'
        )

    def view_pdf_invoice(self, obj): # noqa
        return mark_safe(
            f'<a target="_blank" class="button" '
            f'href="{reverse("pdf_generator:view_pdf_invoice", args=[obj.pk])}">View PDF invoice</a>'
        )


admin.site.register(Offer, OfferAdmin)
