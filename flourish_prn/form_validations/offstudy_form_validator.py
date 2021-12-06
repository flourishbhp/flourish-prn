from django import forms
from django.apps import apps as django_apps
from edc_form_validators import FormValidator
from django.core.exceptions import ObjectDoesNotExist


class OffstudyFormValidator(FormValidator):

    antenantal_enrollment_model = 'flourish_caregiver.antenatalenrollment'

    @property
    def antenantal_enrollment_model_cls(self):
        return django_apps.get_model(self.antenantal_enrollment_model)

    def clean(self):
        super().clean()

        self.validate_other_specify(
            field='reason',
            other_specify_field='reason_other',
        )
        self.validate_against_latest_visit()
        self.validate_preg_subcohotA()

    def validate_preg_subcohotA(self):
        subject_identifier = self.cleaned_data.get('subject_identifier')
        offstudy_point = self.cleaned_data.get('offstudy_point')
        try:
            antenantal_enrollment = self.antenantal_enrollment_model_cls.objects.get(subject_identifier=subject_identifier)
        except ObjectDoesNotExist:
            pass
        else:
            if antenantal_enrollment and offstudy_point == None:
                raise forms.ValidationError({
                        'offstudy_point': 'Question 6 required for pregnant women'
                    })
        


    def validate_against_latest_visit(self):
        self.visit_cls = django_apps.get_model(self.visit_model)

        subject_identifier = self.cleaned_data.get('subject_identifier')
        latest_visit = self.visit_cls.objects.filter(
            appointment__subject_identifier=subject_identifier).order_by(
            '-report_datetime').first()

        report_datetime = self.cleaned_data.get('report_datetime')
        offstudy_date = self.cleaned_data.get('offstudy_date')

        if latest_visit:
            latest_visit_datetime = latest_visit.report_datetime

            if report_datetime < latest_visit.report_datetime:
                raise forms.ValidationError({
                    'report_datetime': 'Report datetime cannot be '
                    f'before previous visit Got {report_datetime} '
                    f'but previous visit is {latest_visit_datetime}'
                })
            if offstudy_date and \
                    offstudy_date < latest_visit.report_datetime.date():
                raise forms.ValidationError({
                    'offstudy_date': 'Offstudy date cannot be '
                    f'before previous visit Got {offstudy_date} '
                    f'but previous visit is {latest_visit_datetime.date()}'
                })
