from django import forms
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidatorMixin

from flourish_form_validations.form_validators import FormValidatorMixin as FlourishFormValidatorMixin

from ..models import ChildDeathReport


class ChildDeathReportForm(FormValidatorMixin, FlourishFormValidatorMixin, forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'subject_identifier')
        self.validate_against_consent_datetime(
            self.cleaned_data.get('report_datetime'))
        super().clean()

    def validate_against_consent(self):
        """Returns an instance of the current maternal consent version form or
        raises an exception if not found."""
        subject_identifier = self.subject_identifier[:-3]

        try:
            consent = self.caregiver_consent_cls.objects.get(
                subject_identifier=subject_identifier,
                version='1')
        except self.caregiver_consent_cls.DoesNotExist:
                raise ValidationError(
                    'Please complete Caregiver Consent form '
                    f'before proceeding.')
        else:
            return consent

    class Meta:
        model = ChildDeathReport
        fields = '__all__'
