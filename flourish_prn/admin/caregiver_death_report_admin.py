from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import flourish_prn_admin
from ..forms import CaregiverDeathReportForm
from ..models import CaregiverDeathReport
from .modeladmin_mixins import ModelAdminMixin


@admin.register(CaregiverDeathReport, site=flourish_prn_admin)
class CaregiverDeathReportAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = CaregiverDeathReportForm

    search_fields = ('subject_identifier',)

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                ]}
         ), audit_fieldset_tuple)

