from datetime import timedelta

from django.shortcuts import render
from django.views.generic.base import TemplateView

from pdf_generator.models import Designation, Offer, Phase, Page

from wkhtmltopdf.views import PDFTemplateView


def offer(request):
    """offer blank template"""
    return render(
        request=request,
        template_name='main_offer.html',
    )


def invoice(request):
    """invoice blank template"""
    return render(
        request=request,
        template_name='main_invoice.html',
    )


class ViewPDF(TemplateView):
    """view pdf"""
    template_name = 'main_invoice.html'
    name = 'pdf'
    pk_url_kwarg = 'id'
    context_object_name = 'offer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offer_number = self.kwargs['id']
        offer = Offer.objects.get(number=offer_number)
        context['offer'] = offer
        context['zahlbar_bis'] = offer.create_date + timedelta(days=30)
        context['netto_price'] = offer.get_netto_price()
        context['mwst'] = offer.get_mwst()
        context['invoice_amount_total'] = offer.get_invoice_amount_total()
        context['designations'] = Designation.objects.filter(
            phase__in=Phase.objects.filter(page__in=Page.objects.filter(offer=offer_number))
        )
        context['num_designations'] = list(range(1, context['designations'].count() + 1))
        context['items'] = list()
        for designation, num in zip(context['designations'], context['num_designations']):
            context['items'].append((designation, num))

        if 'offer' in self.request.build_absolute_uri():
            self.template_name = 'main_offer.html'

        return context


class GetPDF(PDFTemplateView):
    """get pdf file"""
    template_name = 'print_pdf_invoice.html'
    name = 'pdf'
    pk_url_kwarg = 'id'
    context_object_name = 'offer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offer_number = self.kwargs['id']
        offer = Offer.objects.get(number=offer_number)
        context['offer'] = offer
        context['zahlbar_bis'] = offer.create_date + timedelta(days=30)
        context['netto_price'] = offer.get_netto_price()
        context['mwst'] = offer.get_mwst()
        context['invoice_amount_total'] = offer.get_invoice_amount_total()
        context['designations'] = Designation.objects.filter(
            phase__in=Phase.objects.filter(page__in=Page.objects.filter(offer=offer_number))
        )
        context['num_designations'] = list(range(1, context['designations'].count() + 1))
        context['items'] = list()
        for designation, num in zip(context['designations'], context['num_designations']):
            context['items'].append((designation, num))
        self.filename = 'Rechnung_' + str(offer_number) + '.pdf'

        if 'offer' in self.request.build_absolute_uri():
            self.template_name = 'print_pdf_offer.html'
            self.filename = 'Offerte_' + str(offer_number) + '.pdf'

        return context
