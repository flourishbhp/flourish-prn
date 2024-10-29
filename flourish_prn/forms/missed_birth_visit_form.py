from flourish_prn.form_validations.missed_birth_visit_validator import MissedBirthVisitFormValidator
from ..models import MissedBirthVisit
from django import forms
from edc_form_validators import FormValidatorMixin
from flourish_form_validations.form_validators import FormValidatorMixin as FlourishFormValidatorMixin
from django.apps import apps as django_apps


class MissedBirthVisitForm(
        FlourishFormValidatorMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = MissedBirthVisitFormValidator
    antenatal_enrol_model = 'flourish_caregiver.antenatalenrollment'

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    @property
    def antenatal_model_cls(self):
        return django_apps.get_model(self.antenatal_enrol_model)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        child_subject_identifier = self.initial.get('subject_identifier', None)

        antenatal_enrol_obj = self.antenatal_model_cls.objects.filter(
            child_subject_identifier=child_subject_identifier).first()
        if antenatal_enrol_obj:
            if antenatal_enrol_obj.real_time_ga:
                self.initial['gestational_age'] = antenatal_enrol_obj.real_time_ga
                self.fields['gestational_age'].widget = forms.TextInput(
                attrs={'readonly': 'readonly'})

    class Meta:
        model = MissedBirthVisit
        fields = '__all__'
