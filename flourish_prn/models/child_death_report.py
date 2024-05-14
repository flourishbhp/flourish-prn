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

    class Meta:
        app_label = 'flourish_prn'
        verbose_name = 'Child Death Report'
