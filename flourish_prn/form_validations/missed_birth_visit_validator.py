from edc_form_validators import FormValidator
from edc_constants.constants import YES, NO
from django import forms


class MissedBirthVisitFormValidator(FormValidator):

    def clean(self):

        super().clean()

        self.validate_metrics_avail()
        self.validate_apgar_score()
        self.validate_gestational_age()

        self.not_required_if(
           NO,
           field='congenital_anomalities',
           field_required="congenital_anomalities_info", )

    def validate_gestational_age(self):
        """
        Gestional age should be between age of 25 and 45 for the purpose
        of this study
        """
        gestational_age = self.cleaned_data.get('gestational_age', 0)

        if gestational_age:
            if 25 > gestational_age or gestational_age > 45:
                raise forms.ValidationError(
                    {'gestational_age': 'Gestational age should be between 25 and 45.'})

        else:
            raise forms.ValidationError({'gestational_age': 'Gestational age is required'})

    def validate_apgar_score(self):
        agpar_list = ['apgar_score_min_1', 'apgar_score_min_5',
                      'apgar_score_min_10']

        for agpar in agpar_list:
            self.required_if(
                YES,
                field='apgar_score',
                field_required=agpar,
                required_msg='If Apgar scored performed, this field is required.')

    def validate_metrics_avail(self):
        fields_dict = {'weight_avail': 'weight_kg',
                       'length_avail': 'infant_length',
                       'head_circ_avail': 'head_circumference', }

        for field, required_field in fields_dict.items():
            self.required_if(
                YES,
                field=field,
                field_required=required_field)
