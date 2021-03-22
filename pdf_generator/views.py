from datetime import timedelta
from django.http import FileResponse, Http404, HttpResponse
import PyPDF2
from django.contrib import messages
from django.shortcuts import redirect

from pdf_generator.models import Designation, Offer, Page, Phase, Invoice

from wkhtmltopdf.views import PDFTemplateView, PDFTemplateResponse

from pdf_generator.utils import remove_blank_page


class GetPDF(PDFTemplateView):
    """get or see pdf file"""
    pk_url_kwarg = 'id'
    context_object_name = 'offer'
    template_name = 'print_pdf_base.html'

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
        # self.filename = 'Rechnung_' + str(offer_number) + '.pdf'
        context['number_of_pages'] = Page.objects.filter(offer=offer_number).count()

        invoice = Invoice.objects.update_or_create(
            offer=offer,
            number=offer.number,
            defaults={
                'client_address': offer.client_address,
                'client_name': offer.client_name,
                'email': offer.email,
                'description': offer.description,
                'iban': offer.iban,
                'bic_swift': offer.bic_swift,
                'kontonummer': offer.kontonummer,
                'bemerkung': offer.bemerkung,
                'zahlbar_bis': offer.create_date + timedelta(days=30),
                'netto_price': offer.get_netto_price(),
                'mwst': offer.get_mwst(),
                'invoice_amount_total': offer.get_invoice_amount_total(),
                'create_date': offer.create_date
            }
        )

        invoice[0].save()
        context['invoice'] = invoice[0]

        if context['number_of_pages'] == 1:

            if 'view_pdf_invoice' in self.request.build_absolute_uri():
                self.template_name = 'print_pdf_invoice_one_page.html'
                self.show_content_in_browser = True
                self.filename = 'Rechnung_' + str(offer_number) + '.pdf'

            if 'get_pdf_invoice' in self.request.build_absolute_uri():
                self.template_name = 'print_pdf_invoice_one_page.html'
                self.filename = 'Rechnung_' + str(offer_number) + '.pdf'

            if 'view_pdf_offer' in self.request.build_absolute_uri():
                self.template_name = 'print_pdf_offer_one_page.html'
                self.show_content_in_browser = True
                self.filename = 'Offerte_' + str(offer_number) + '.pdf'

            if 'get_pdf_offer' in self.request.build_absolute_uri():
                self.template_name = 'print_pdf_offer_one_page.html'
                self.filename = 'Offerte_' + str(offer_number) + '.pdf'

        elif context['number_of_pages'] > 1:

            if 'view_pdf_invoice' in self.request.build_absolute_uri():
                self.template_name = 'top_invoice.html'
                self.show_content_in_browser = True
                self.filename = 'Rechnung_' + str(offer_number) + '.pdf'

            if 'get_pdf_invoice' in self.request.build_absolute_uri():
                self.template_name = 'top_invoice.html'
                self.filename = 'Rechnung_' + str(offer_number) + '.pdf'

            if 'view_pdf_offer' in self.request.build_absolute_uri():
                self.template_name = 'top_offer.html'
                self.show_content_in_browser = True
                self.filename = 'Offerte_' + str(offer_number) + '.pdf'

            if 'get_pdf_offer' in self.request.build_absolute_uri():
                self.template_name = 'top_offer.html'
                self.filename = 'Offerte_' + str(offer_number) + '.pdf'

        return context

    def render_to_response(self, context, **response_kwargs):
        """delete blank page at end of file, save file, return file"""
        response = super().render_to_response(context, **response_kwargs)
        with open(f"media/results/test_{self.filename}", "wb") as f:
            f.write(response.rendered_content)
        remove_blank_page(self.filename)

        if 'view_pdf' in self.request.build_absolute_uri():
            with open(f"media/results/{self.filename}", 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/pdf')
            return response

        elif 'get_pdf' in self.request.build_absolute_uri():
            with open(f"media/results/{self.filename}", 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/pdf')
                response['Content-Disposition'] = "attachment; filename=" + self.filename
            return response


def create_update_invoice(request, id):
    """create an invoice based on an offer"""
    offer_number = id
    offer = Offer.objects.get(number=offer_number)

    invoice = Invoice.objects.update_or_create(
        offer=offer,
        number=offer.number,
        defaults={
            'client_address': offer.client_address,
            'client_name': offer.client_name,
            'email': offer.email,
            'description': offer.description,
            'iban': offer.iban,
            'bic_swift': offer.bic_swift,
            'kontonummer': offer.kontonummer,
            'bemerkung': offer.bemerkung,
            'zahlbar_bis': offer.create_date + timedelta(days=30),
            'netto_price': offer.get_netto_price(),
            'mwst': offer.get_mwst(),
            'invoice_amount_total': offer.get_invoice_amount_total(),
            'create_date': offer.create_date
        }
    )

    invoice[0].save()
    messages.info(request, 'Invoice has been successfully updated. Go to the "Invoice" section')

    return redirect(request.META['HTTP_REFERER'])
