from django.urls import path

from . import views
from .views import GetPDFoffer

app_name = "pdf_generator"

urlpatterns = [
    path('offer', views.offer, name='offer'),
    path('get_pdf_offer/<int:id>', GetPDFoffer.as_view(), name='get_pdf_offer')
]
