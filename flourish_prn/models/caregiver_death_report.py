from django.db import models
from edc_action_item.model_mixins.action_model_mixin import ActionModelMixin
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators.date import datetime_not_future
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_identifier.managers import SubjectIdentifierManager
from edc_protocol.validators import datetime_not_before_study_start
from edc_search.model_mixins import SearchSlugModelMixin

from ..action_items import CAREGIVER_DEATH_REPORT_ACTION
from .death_report_mixin import DeathReportModelMixin


class CaregiverDeathReport(DeathReportModelMixin,
                        SiteModelMixin,
                        ActionModelMixin,
                        SearchSlugModelMixin,
                        BaseUuidModel):

    tracking_identifier_prefix = 'MO'

    action_name = CAREGIVER_DEATH_REPORT_ACTION

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.subject_identifier,)

    natural_key.dependencies = ['sites.Site']

    class Meta:
        app_label = 'flourish_prn'
        verbose_name = 'Death Report'
