from django import forms
from edc_form_validators import FormValidatorMixin

from flourish_form_validations.form_validators import FormValidatorMixin as FlourishFormValidatorMixin

from ..form_validations import OffstudyFormValidator
from ..models import CaregiverOffStudy


class CaregiverOffStudyForm(FlourishFormValidatorMixin, FormValidatorMixin, forms.ModelForm):

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

    class Meta:
        model = CaregiverOffStudy
        fields = '__all__'
