from django import forms
from django.forms import BaseInlineFormSet, ModelForm, modelformset_factory

from pdf_generator.models import Designation, Offer


class DesignationAdminForm(forms.ModelForm):

    class Meta:
        model = Designation
        fields = '__all__'


class DesignationForm(ModelForm):

    class Meta:
        model = Designation
        fields = '__all__'


class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = '__all__'

    def clean(self):
        pass


class DesignationInlineFormSet(BaseInlineFormSet):
    def clean(self):
        pass


DesignationFormSet = modelformset_factory(
    model=Designation,
    form=DesignationForm,
    extra=0
)
