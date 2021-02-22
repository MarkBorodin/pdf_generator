from django.contrib import admin
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


class OfferAdmin(admin.ModelAdmin):
    inlines = (DesignationsInline,)
    list_display = (
        'number', 'create_date', 'client_address', 'client_name', 'client_address', 'email', 'description', 'get_pdf'
    )
    search_fields = ('number', 'create_date', 'client_address', 'client_name', 'client_address', 'email', 'description')
    list_filter = ('number', 'create_date', 'client_address', 'client_name', 'email', 'description')
    fields = ('client_address', 'client_name', 'email', 'description')

    def get_pdf(self, obj):
        return mark_safe(
            f'<a class="button" href="{reverse("pdf_generator:get_pdf_offer", args=[obj.pk])}">Get PDF</a>'
        )


admin.site.register(Offer, OfferAdmin)
admin.site.register(Designation)
