from django.urls import path

from .views import GetPDF, create_update_invoice, create_update_offer_confirmation, view_signed_file

app_name = "pdf_generator"

urlpatterns = [
    # offer
    path('get_pdf_offer/<int:id>', GetPDF.as_view(), name='get_pdf_offer'),
    path('view_pdf_offer/<int:id>', GetPDF.as_view(), name='view_pdf_offer'),
    path('create_invoice/<int:id>', create_update_invoice, name='create_invoice'),
    path('update_invoice/<int:id>', create_update_invoice, name='update_invoice'),
    path('create_offer_confirmation/<int:id>', create_update_offer_confirmation, name='create_offer_confirmation'),
    path('update_offer_confirmation/<int:id>', create_update_offer_confirmation, name='update_offer_confirmation'),

    # invoice
    path('get_pdf_invoice/<int:id>', GetPDF.as_view(), name='get_pdf_invoice'),
    path('view_pdf_invoice/<int:id>', GetPDF.as_view(), name='view_pdf_invoice'),

    # order_confirmation
    path('get_pdf_confirmation/<int:id>', GetPDF.as_view(), name='get_pdf_confirmation'),
    path('view_pdf_confirmation/<int:id>', GetPDF.as_view(), name='view_pdf_confirmation'),
    path('view_signed_file/<int:id>', view_signed_file, name='view_signed_file'),
]
