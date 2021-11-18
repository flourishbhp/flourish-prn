from edc_action_item.model_mixins.action_model_mixin import ActionModelMixin
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_identifier.managers import SubjectIdentifierManager
from edc_search.model_mixins import SearchSlugModelMixin

from ..action_items import DEATH_REPORT_ACTION


class DeathReport(ActionModelMixin,
                        SiteModelMixin,
                        SearchSlugModelMixin,
                        BaseUuidModel):

    tracking_identifier_prefix = 'MO'

    action_name = DEATH_REPORT_ACTION

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.subject_identifier,)

    natural_key.dependencies = ['sites.Site']

    class Meta:
        app_label = 'flourish_prn'
        verbose_name = 'Death Report'
