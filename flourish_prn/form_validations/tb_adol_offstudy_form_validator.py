from ..form_validations import OffstudyFormValidator
from django.apps import apps as django_apps
from django import forms
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator

class TBAdolOffstudyValidator(OffstudyFormValidator,FormValidator):
    def clean(self):
        self.subject_identifier = self.cleaned_data.get('subject_identifier')
        super().clean()
        self.validate_offstudy_date()
        

                
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
                    f"Offstudy date {offstudy_date} cannot be before Assent datetime "
                    f"{tb_adol_assent.consent_datetime.date()}.")
            

    def validate_against_latest_visit(self):

        self.visit_cls = django_apps.get_model('flourish_child.childvisit')
        if not self.subject_identifier:
            return None
        latest_visit =self.visit_cls.objects.filter(
            appointment__subject_identifier=self.subject_identifier,
            schedule_name__icontains='tb_adol'
        ).order_by('-report_datetime').first()

        super().validate_against_latest_visit(latest_visit)
    

    
    

                

    