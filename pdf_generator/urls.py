from django.urls import path

from .views import GetPDF, create_update_invoice

app_name = "pdf_generator"

urlpatterns = [
    # offer
    path('get_pdf_offer/<int:id>', GetPDF.as_view(), name='get_pdf_offer'),
    path('view_pdf_offer/<int:id>', GetPDF.as_view(), name='view_pdf_offer'),
    path('create_invoice/<int:id>', create_update_invoice, name='create_invoice'),
    path('update_invoice/<int:id>', create_update_invoice, name='update_invoice'),

    # invoice
    path('get_pdf_invoice/<int:id>', GetPDF.as_view(), name='get_pdf_invoice'),
    path('view_pdf_invoice/<int:id>', GetPDF.as_view(), name='view_pdf_invoice'),
]
