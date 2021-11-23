from django import forms
from edc_form_validators import FormValidatorMixin
from flourish_form_validations.form_validators.form_validator_mixin import (
    FlourishFormValidatorMixin)
from ..models import CaregiverDeathReport


class CaregiverDeathReportForm(FormValidatorMixin, FlourishFormValidatorMixin, forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'subject_identifier')
        self.validate_against_consent_datetime(
            self.cleaned_data.get('report_datetime'))
        super().clean()

    class Meta:
        model = CaregiverDeathReport
        fields = '__all__'
