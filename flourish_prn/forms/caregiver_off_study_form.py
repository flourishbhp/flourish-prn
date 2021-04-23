from django.apps import apps as django_apps
from django import forms
from edc_form_validators import FormValidatorMixin
from flourish_form_validations.form_validators.form_validator_mixin import (
    FlourishFormValidatorMixin)

from ..form_validations import OffstudyFormValidator
from ..models import CaregiverOffStudy


class CaregiverOffStudyForm(FormValidatorMixin, FlourishFormValidatorMixin,
                             forms.ModelForm):

    OffstudyFormValidator.visit_model = 'flourish_caregiver.maternalvisit'

    preg_women_screening_model = 'flourish_caregiver.screeningpregwomen'

    form_validator_cls = OffstudyFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        self.subject_identifier = self.cleaned_data.get('subject_identifier')

        super().clean()
        self.validate_against_consent_datetime(
            self.cleaned_data.get('report_datetime'))

        offstudy_point = self.cleaned_data.get('offstudy_point')

        if self.preg_women_screening and not offstudy_point:
            message = {'offstudy_point': 'This field is required.'}
            raise forms.ValidationError(message)
        elif not self.preg_women_screening and offstudy_point:
            message = {'offstudy_point': 'This field is not required.'}
            raise forms.ValidationError(message)

    @property
    def preg_women_screening_cls(self):
        return django_apps.get_model(self.preg_women_screening_model)

    @property
    def preg_women_screening(self):
        try:
            self.preg_women_screening_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except self.preg_women_screening_cls.DoesNotExist:
            return False
        else:
            return True

    class Meta:
        model = CaregiverOffStudy
        fields = '__all__'
