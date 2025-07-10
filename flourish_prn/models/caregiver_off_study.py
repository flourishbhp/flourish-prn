from django.apps import apps as django_apps
from django.db import models
from django.db.models import Q
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators.date import datetime_not_future
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO_NA, NOT_APPLICABLE
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

    future_studies = models.CharField(
        verbose_name=('We recognize you stated you are interested in future '
                      'studies. Is that still the case? '),
        max_length=3,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE)

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    @property
    def onschedules(self):
        onschedules = []
        history_model = 'edc_visit_schedule.subjectschedulehistory'
        history_cls = django_apps.get_model(history_model)

        schedules = history_cls.objects.filter(
            (Q(offschedule_datetime__gte=self.report_datetime) |
             Q(offschedule_datetime__isnull=True)),
            subject_identifier=self.subject_identifier,
            onschedule_datetime__lte=self.report_datetime)

        for obj in schedules:
            onschedule_model_cls = django_apps.get_model(
                obj.onschedule_model)
            onschedules.append(
                onschedule_model_cls.objects.get(
                    subject_identifier=self.subject_identifier,
                    schedule_name=obj.schedule_name))
        return onschedules

    def take_off_schedule(self):
        for onschedule in self.onschedules:
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
