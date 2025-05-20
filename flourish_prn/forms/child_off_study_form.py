from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidatorMixin

from flourish_child_validations.form_validators import ChildFormValidatorMixin

from ..form_validations import OffstudyFormValidator
from ..models import ChildOffStudy


class ChildOffStudyForm(FormValidatorMixin, forms.ModelForm):
    OffstudyFormValidator.visit_model = 'flourish_child.childvisit'

    form_validator_cls = OffstudyFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    cohort_model = 'flourish_caregiver.cohort'

    @property
    def cohort_model_cls(self):
        return django_apps.get_model(self.cohort_model)

    def clean(self):
        self.infant_identifier = self.cleaned_data.get('subject_identifier')
        super().clean()

        self.validate_offstudy_date()

        self.validate_against_childage()

    def validate_offstudy_date(self):
        offstudy_date = self.cleaned_data.get('offstudy_date')

        dummy_consent_model_cls = django_apps.get_model(
            'flourish_child.childdummysubjectconsent')
        try:
            dummy_consent = dummy_consent_model_cls.objects.filter(
                subject_identifier=self.infant_identifier).latest('consent_datetime')
        except dummy_consent_model_cls.DoesNotExist:
            raise ValidationError('Dummy Consent does not exist.')
        else:
            if offstudy_date and offstudy_date < dummy_consent.report_datetime.date():
                raise forms.ValidationError(
                    "Offstudy date cannot be before enrollment datetime.")

    def validate_against_childage(self):
        reason = self.cleaned_data.get('reason')
        try:
            cohort = self.cohort_model_cls.objects.filter(
                subject_identifier=self.infant_identifier).latest(
                    'assign_datetime')
        except self.cohort_model_cls.DoesNotExist:
            pass
        else:
            child_age = cohort.child_age
            if (child_age and child_age < 18 and
                    reason in ['18_na_reconsent', '18_no_contact']):
                raise forms.ValidationError(
                    {'reason': 'Child is less than 18 years of age'})

    class Meta:
        model = ChildOffStudy
        fields = '__all__'
