from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db import models
from django.forms import Textarea, EmailField
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
        'number', 'create_date', 'client_name', 'client_address', 'email', 'description', 'view_pdf', 'get_pdf'
    )
    search_fields = ('number', 'create_date', 'client_address', 'client_name', 'client_address', 'email', 'description')
    list_filter = ('number', 'create_date', 'client_address', 'client_name', 'email', 'description')
    fields = ('client_address', 'client_name', 'email', 'description')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 170})},
        models.EmailField: {'widget': Textarea(attrs={'rows': 1, 'cols': 170})},
    }

    def get_pdf(self, obj): # noqa
        return mark_safe(
            f'<a class="button" href="{reverse("pdf_generator:get_pdf_offer", args=[obj.pk])}">Get PDF</a>'
        )

    def view_pdf(self, obj): # noqa
        return mark_safe(
            f'<a target="_blank" class="button" '
            f'href="{reverse("pdf_generator:view_pdf_offer", args=[obj.pk])}">View PDF</a>'
        )


admin.site.register(Offer, OfferAdmin)
