from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.db import models
from edc_action_item.model_mixins.action_model_mixin import ActionModelMixin
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_search.model_mixins import SearchSlugModelMixin

from ..action_items import CHILD_DEATH_REPORT_ACTION
from ..choices import RELATIONSHIP_CHOICES
from .death_report_mixin import DeathReportModelMixin


class ChildDeathReport(DeathReportModelMixin, ActionModelMixin,
                        SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):

    ''' A model completed by the user after an infant's death. '''

    tracking_identifier_prefix = 'ID'

    action_name = CHILD_DEATH_REPORT_ACTION

    study_drug_relationship = models.CharField(
        verbose_name=('Relationship between the infant\'s death and '
                      '(CTX vs Placebo) '),
        max_length=20,
        choices=RELATIONSHIP_CHOICES)

    infant_nvp_relationship = models.CharField(
        verbose_name=('Relationship between the infant\'s death and '
                      'infant extended nevirapine prophylaxis '),
        max_length=20,
        choices=RELATIONSHIP_CHOICES)

    haart_relationship = models.CharField(
        verbose_name=('Relationship between the infant\'s death and '
                      'HAART '),
        max_length=20,
        choices=RELATIONSHIP_CHOICES)

    trad_med_relationship = models.CharField(
        verbose_name=('Relationship between the infant\'s death and '
                      'traditional medicine use '),
        max_length=20,
        choices=RELATIONSHIP_CHOICES)

    history = HistoricalRecords()

    def get_consent_version(self):
        consent_version_cls = django_apps.get_model(
            'flourish.flourishconsentversion')
        try:
            consent_version_obj = consent_version_cls.objects.get(
                screening_identifier=self.subject_identifier)
        except consent_version_cls.DoesNotExist:
            raise ValidationError(
                'Missing Consent Version form. Please complete '
                'it before proceeding.')
        return consent_version_obj.version

    class Meta:
        app_label = 'flourish_prn'
        verbose_name = 'Child Death Report'
