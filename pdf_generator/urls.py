from django.urls import path

from . import views
from .views import GetPDFoffer, ViewPDFoffer, ViewPDFinvoice, GetPDFinvoice

app_name = "pdf_generator"

urlpatterns = [
    path('offer', views.offer, name='offer'),
    path('invoice', views.offer, name='invoice'),

    path('get_pdf_offer/<int:id>', GetPDFoffer.as_view(), name='get_pdf_offer'),
    path('view_pdf_offer/<int:id>', ViewPDFoffer.as_view(), name='view_pdf_offer'),

    path('get_pdf_invoice/<int:id>', GetPDFinvoice.as_view(), name='get_pdf_invoice'),
    path('view_pdf_invoice/<int:id>', ViewPDFinvoice.as_view(), name='view_pdf_invoice'),
]
