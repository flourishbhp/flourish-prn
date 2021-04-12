from django.conf import settings
from django.contrib import admin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_metadata import NextFormGetter
from edc_model_admin import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminInstitutionMixin,
    ModelAdminRedirectOnDeleteMixin)
from edc_model_admin import audit_fieldset_tuple
from edc_subject_dashboard import ModelAdminSubjectDashboardMixin

from ..admin_site import flourish_prn_admin
from ..forms import CaregiverOffStudyForm
from ..models import CaregiverOffStudy
from .exportaction_mixin import ExportActionMixin


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin,
                      ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin,
                      ModelAdminInstitutionMixin,
                      ModelAdminRedirectOnDeleteMixin,
                      ModelAdminSubjectDashboardMixin,
                      ModelAdminSiteMixin, ExportActionMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'
    next_form_getter_cls = NextFormGetter
    subject_dashboard_url = 'subject_dashboard_url'

    post_url_on_delete_name = settings.DASHBOARD_URL_NAMES.get(
        subject_dashboard_url)

    def post_url_on_delete_kwargs(self, request, obj):
        return dict(subject_identifier=obj.subject_identifier)


@admin.register(CaregiverOffStudy, site=flourish_prn_admin)
class CaregiverOffStudyAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = CaregiverOffStudyForm

    search_fields = ('subject_identifier',)

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                'offstudy_date',
                'reason',
                'reason_other',
                'offstudy_point',
                'comment']}
         ), audit_fieldset_tuple)

    radio_fields = {'reason': admin.VERTICAL,
                    'offstudy_point': admin.VERTICAL}