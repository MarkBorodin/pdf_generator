from django.urls import path

from . import views
from .views import GetPDF, ViewPDF

app_name = "pdf_generator"

urlpatterns = [
    # offer
    path('offer', views.offer, name='offer'),
    path('get_pdf_offer/<int:id>', GetPDF.as_view(), name='get_pdf_offer'),
    path('view_pdf_offer/<int:id>', ViewPDF.as_view(), name='view_pdf_offer'),

    # invoice
    path('invoice', views.offer, name='invoice'),
    path('get_pdf_invoice/<int:id>', GetPDF.as_view(), name='get_pdf_invoice'),
    path('view_pdf_invoice/<int:id>', ViewPDF.as_view(), name='view_pdf_invoice'),
]
