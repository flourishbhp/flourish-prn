from django import forms
from flourish_prn.form_validations.tb_adol_offstudy_form_validator import TBAdolOffstudyValidator
from flourish_prn.models import TBAdolOffStudy
from edc_form_validators import FormValidatorMixin

class TBAdolOffStudyForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = TBAdolOffstudyValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))


    class Meta:
        model = TBAdolOffStudy
        fields = '__all__'
