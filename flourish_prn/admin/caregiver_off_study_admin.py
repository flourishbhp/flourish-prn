import pytz
from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_constants.constants import YES
from edc_fieldsets import FieldsetsModelAdminMixin
from edc_fieldsets.fieldlist import Remove
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


tz = pytz.timezone('Africa/Gaborone')


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
class CaregiverOffStudyAdmin(ModelAdminMixin,  FieldsetsModelAdminMixin,
                             admin.ModelAdmin):

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
                'future_studies',
                'results_method',
                'results_dt',
                'comment']}
         ), audit_fieldset_tuple)

    radio_fields = {'reason': admin.VERTICAL,
                    'offstudy_point': admin.VERTICAL,
                    'future_studies': admin.VERTICAL,
                    'results_method': admin.VERTICAL}

    conditional_fieldlists = {
        'not_interested': Remove('future_studies')}

    def get_key(self, request, obj=None):
        subject_identifier = request.GET.get(
            'subject_identifier', None)
        model_obj = self.get_subject_consent(subject_identifier)
        future_contact = getattr(model_obj, 'future_contact', None)
        if future_contact != YES:
            return 'not_interested'

    def get_subject_consent(self, subject_identifier):
        consent_cls = django_apps.get_model(
            'flourish_caregiver.subjectconsent')
        try:
            model_obj = consent_cls.objects.filter(
                subject_identifier=subject_identifier).earliest(
                    'consent_datetime')
        except consent_cls.DoesNotExist:
            return None
        else:
            return model_obj

    def offstudy_extra_details(self, subject_identifier):
        model_obj = self.get_subject_consent(subject_identifier)
        consent_dt = getattr(model_obj, 'consent_datetime', None)
        if consent_dt:
            consent_dt = consent_dt.astimezone(tz).strftime('%d-%B-%Y')
            return mark_safe(
                f'Thank you for participating since <b>{consent_dt}</b>, '
                'we will be concluding the study, and you will be taken '
                'off-study today. We will not be collecting any additional '
                'study data as of today, however the team will inform you '
                'about the study results today.')

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        subject_identifier = request.GET.get('subject_identifier', None)
        extra_context['offstudy_script'] = self.offstudy_extra_details(
            subject_identifier)

        return super().add_view(
            request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        subject_identifier = request.GET.get('subject_identifier', None)
        extra_context['offstudy_script'] = self.offstudy_extra_details(
            subject_identifier)

        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)
