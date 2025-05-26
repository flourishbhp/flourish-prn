from django import forms
from django.apps import apps as django_apps
from flourish_prn.form_validations.tb_adol_offstudy_form_validator import TBAdolOffstudyValidator
from flourish_prn.forms import ChildOffStudyForm
from flourish_prn.models import TBAdolOffStudy
from edc_form_validators import FormValidator
from django.core.exceptions import ValidationError

class TBAdolOffStudyForm(ChildOffStudyForm,FormValidator, forms.ModelForm):
    form_validator_cls = TBAdolOffstudyValidator

    def clean(self):
        self.subject_identifier = self.cleaned_data.get('subject_identifier')
        super().clean()


    def validate_offstudy_date(self):
        offstudy_date = self.cleaned_data.get('offstudy_date')
       
        tb_adol_assent_model_cls = django_apps.get_model(
            'flourish_child.tbadolassent')
        
        try:
            tb_adol_assent = tb_adol_assent_model_cls.objects.filter(
                subject_identifier=self.subject_identifier).latest('consent_datetime')
        except tb_adol_assent_model_cls.DoesNotExist:
            raise ValidationError('Tb adol Assent does not exist.')
        else:
            if offstudy_date and offstudy_date < tb_adol_assent.consent_datetime.date():
                raise forms.ValidationError(
                    "Offstudy date cannot be before Assent datetime.")
    class Meta:
        model = TBAdolOffStudy
        fields = '__all__'
