from ..form_validations import OffstudyFormValidator
from django.apps import apps as django_apps
from django import forms


class TBAdolOffstudyValidator(OffstudyFormValidator):
    def clean(self):
            super().clean()

    def validate_against_latest_visit(self):
            self.visit_cls = django_apps.get_model(
                'flourish_child.childvisit')

            subject_identifier = self.cleaned_data.get('subject_identifier')
            latest_visit = self.visit_cls.objects.filter(
                appointment__subject_identifier=subject_identifier,
                schedule_name__icontains='tb_adol').order_by(
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
                

    