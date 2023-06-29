from flourish_prn.form_validations.missed_birth_visit_validator import MissedBirthVisitFormValidator
from ..models import MissedBirthVisit
from django import forms
from edc_form_validators import FormValidatorMixin
from flourish_form_validations.form_validators import FormValidatorMixin as FlourishFormValidatorMixin
from django.apps import apps as django_apps

class MissedBirthVisitForm(FlourishFormValidatorMixin,FormValidatorMixin,forms.ModelForm):

    form_validator_cls = MissedBirthVisitFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def __init__(self, *args, **kwargs):
        super(MissedBirthVisitForm, self).__init__(*args, **kwargs)

        subject_identifier = self.initial.get('subject_identifier', None)

        if not subject_identifier:
            return
    
        ultrasound_cls = django_apps.get_model('flourish_caregiver.ultrasound')

        ultrasound_obj = ultrasound_cls.objects.filter(subject_identifier = subject_identifier)

        if ultrasound_obj:

            self.initial['gestation_age'] = ultrasound_obj.ga_by_ultrasound_wks

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'subject_identifier')
        self.validate_against_consent_datetime(
            self.cleaned_data.get('report_datetime'))
        super().clean()


    class Meta:
        model = MissedBirthVisit
        fields = '__all__'

