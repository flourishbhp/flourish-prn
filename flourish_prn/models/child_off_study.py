from django.apps import apps as django_apps
from django.db import models
from edc_action_item.model_mixins.action_model_mixin import ActionModelMixin
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators.date import datetime_not_future
from edc_base.utils import get_utcnow
from edc_identifier.managers import SubjectIdentifierManager
from edc_protocol.validators import datetime_not_before_study_start

from edc_visit_schedule.model_mixins import OffScheduleModelMixin
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from ..action_items import CHILDOFF_STUDY_ACTION
from ..choices import CHILD_OFF_STUDY_REASON
from .offstudy_model_mixin import OffStudyModelMixin


class ChildOffStudy(OffStudyModelMixin, OffScheduleModelMixin,
                    ActionModelMixin, BaseUuidModel):

    """ A model completed by the user when the child is taken off study. """

    tracking_identifier_prefix = 'CO'

    action_name = CHILDOFF_STUDY_ACTION

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        default=get_utcnow,
        help_text=('If reporting today, use today\'s date/time, otherwise use'
                   ' the date/time this information was reported.'))

    reason = models.CharField(
        verbose_name=('Please code the primary reason the participant is'
                      ' being taken off the study'),
        max_length=115,
        choices=CHILD_OFF_STUDY_REASON)

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    def take_off_schedule(self):

        cohorts = ['cohortaenrollment', 'cohortabirth', 'cohortaquarterly',
                   'cohortbenrollment', 'cohortbquarterly',
                   'cohortcenrollment', 'cohortcquarterly', 'cohortcpool',
                   'dyada', 'dyadb', 'dyadc']

        for cohort in cohorts:
            onschedule_model = 'flourish_child.onschedulechild' + cohort
            onschedule_model_cls = django_apps.get_model(onschedule_model)
            on_schedule_objs = onschedule_model_cls.objects.filter(
                subject_identifier=self.subject_identifier)
            if on_schedule_objs:
                for on_schedule_obj in on_schedule_objs:
                    _, schedule = \
                        site_visit_schedules.get_by_onschedule_model_schedule_name(
                            onschedule_model=onschedule_model_cls._meta.label_lower,
                            name=on_schedule_obj.schedule_name)
                    schedule.take_off_schedule(offschedule_model_obj=self)

    class Meta:
        app_label = 'flourish_prn'
        verbose_name = "Child Off-Study"
        verbose_name_plural = "Child Off-Study"
