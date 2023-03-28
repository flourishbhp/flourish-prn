from django import forms
from edc_form_validators import FormValidatorMixin

from flourish_form_validations.form_validators import FormValidatorMixin as FlourishFormValidatorMixin

from ..form_validations import TbReferralAdolFormValidator
from ..models import TbReferalAdol


class TbReferralAdolForm(FormValidatorMixin, FlourishFormValidatorMixin, forms.ModelForm):

    form_validator_cls = TbReferralAdolFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        self.subject_identifier = self.cleaned_data.get('subject_identifier')

        super().clean()

    class Meta:
        model = TbReferalAdol
        fields = '__all__'
