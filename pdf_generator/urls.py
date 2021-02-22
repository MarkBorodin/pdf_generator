from django.urls import path

from . import views
from .views import GetPDFoffer, ViewPDFoffer

app_name = "pdf_generator"

urlpatterns = [
    path('offer', views.offer, name='offer'),
    path('get_pdf_offer/<int:id>', GetPDFoffer.as_view(), name='get_pdf_offer'),
    path('view_pdf_offer/<int:id>', ViewPDFoffer.as_view(), name='view_pdf_offer'),
]
