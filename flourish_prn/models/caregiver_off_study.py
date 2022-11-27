from django.apps import apps as django_apps
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators.date import datetime_not_future
from edc_base.utils import get_utcnow
from edc_identifier.managers import SubjectIdentifierManager
from edc_protocol.validators import datetime_not_before_study_start

from edc_action_item.model_mixins import ActionModelMixin
from edc_visit_schedule.model_mixins import OffScheduleModelMixin
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from ..action_items import CAREGIVEROFF_STUDY_ACTION
from ..choices import CAREGIVER_OFF_STUDY_REASON, OFFSTUDY_POINT
from .offstudy_model_mixin import OffStudyModelMixin


class CaregiverOffStudy(OffStudyModelMixin, OffScheduleModelMixin,
                        ActionModelMixin, BaseUuidModel):

    tracking_identifier_prefix = 'MO'

    action_name = CAREGIVEROFF_STUDY_ACTION

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        default=get_utcnow,
        help_text=('If reporting today, use today\'s date/time, otherwise use'
                   ' the date/time this information was reported.'))

    reason = models.CharField(
        verbose_name=('Please code the primary reason participant taken'
                      ' off-study'),
        max_length=115,
        choices=CAREGIVER_OFF_STUDY_REASON)

    offstudy_point = models.CharField(
        verbose_name='At what point did the mother go off study',
        choices=OFFSTUDY_POINT,
        max_length=50,
        blank=True, null=True,
        help_text='For pregnant women enrolled in Cohort A')

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    def take_off_schedule(self):
        history_model = 'edc_visit_schedule.subjectschedulehistory'
        history_cls = django_apps.get_model(history_model)
        onschedules = history_cls.objects.onschedules(
            subject_identifier=self.subject_identifier,
            report_datetime=self.report_datetime)

        if onschedules:
            for onschedule in onschedules:
                _, schedule = \
                    site_visit_schedules.get_by_onschedule_model_schedule_name(
                        onschedule_model=onschedule._meta.label_lower,
                        name=onschedule.schedule_name)

                schedule.take_off_schedule(
                    subject_identifier=self.subject_identifier,
                    offschedule_datetime=self.report_datetime,
                    schedule_name=onschedule.schedule_name)

    class Meta:
        app_label = 'flourish_prn'
        verbose_name = 'Caregiver Off Study'
        verbose_name_plural = 'Caregiver Off Study'
