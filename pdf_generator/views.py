from django.shortcuts import render

from pdf_generator.models import Designation, Offer

from wkhtmltopdf.views import PDFTemplateView


def offer(request):
    """offer"""
    return render(
        request=request,
        template_name='main_offer.html'
    )


class GetPDFoffer(PDFTemplateView):
    filename = 'my_pdf.pdf'
    template_name = 'print_pdf_offer.html'
    name = 'pdf'
    pk_url_kwarg = 'id'
    context_object_name = 'offer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offer_number = self.kwargs['id']
        offer = Offer.objects.get(number=offer_number)
        context['offer'] = offer
        context['netto_price'] = offer.get_netto_price()
        context['mwst'] = offer.get_mwst()
        context['invoice_amount_total'] = offer.get_invoice_amount_total()
        context['designations'] = Designation.objects.filter(offer=offer_number)
        context['num_designations'] = list(range(1, Designation.objects.filter(offer=offer_number).count() + 1))
        context['items'] = list()
        for designation, num in zip(context['designations'], context['num_designations']):
            context['items'].append((designation, num))
        return context
