from django.forms import BaseInlineFormSet, ModelForm, modelformset_factory

from pdf_generator.models import Designation


class DesignationForm(ModelForm):

    class Meta:
        model = Designation
        fields = '__all__'


class DesignationInlineFormSet(BaseInlineFormSet):
    def clean(self):
        pass


DesignationFormSet = modelformset_factory(
    model=Designation,
    form=DesignationForm,
    extra=0
)
