from django.apps import apps as django_apps
from django import forms
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidatorMixin

from flourish_child_validations.form_validators import ChildFormValidatorMixin

from ..form_validations import OffstudyFormValidator
from ..models import ChildOffStudy


class ChildOffStudyForm(FormValidatorMixin, ChildFormValidatorMixin,
                        forms.ModelForm):

    OffstudyFormValidator.visit_model = 'flourish_child.childvisit'

    form_validator_cls = OffstudyFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        self.infant_identifier = self.cleaned_data.get('subject_identifier')
        super().clean()

        self.validate_offstudy_date()

    def validate_offstudy_date(self):
        offstudy_date = self.cleaned_data.get('offstudy_date')

        dummy_consent_model_cls = django_apps.get_model(
            'flourish_child.childdummysubjectconsent')
        try:
            dummy_consent = dummy_consent_model_cls.objects.get(
                subject_identifier=self.infant_identifier).latest('consent_datetime')
        except dummy_consent_model_cls.DoesNotExist:
            raise ValidationError('Dummy Consent does not exist.')
        else:
            if offstudy_date and offstudy_date < dummy_consent.report_datetime.date():
                raise forms.ValidationError(
                    "Offstudy date cannot be before enrollment datetime.")

    class Meta:
        model = ChildOffStudy
        fields = '__all__'
