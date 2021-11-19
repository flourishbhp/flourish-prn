from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import flourish_prn_admin
from ..forms import ChildDeathReportForm
from ..models import ChildDeathReport
from .modeladmin_mixins import ModelAdminMixin


@admin.register(ChildDeathReport, site=flourish_prn_admin)
class ChildDeathReportAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ChildDeathReportForm

    search_fields = ('subject_identifier',)

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                'death_date',
                'cause',
                'cause_other',
                'perform_autopsy',
                'death_cause',
                'cause_category',
                'cause_category_other',
                'illness_duration',
                'medical_responsibility',
                'participant_hospitalized',
                'reason_hospitalized',
                'reason_hospitalized_other',
                'days_hospitalized',
                'study_drug_relationship',
                'infant_nvp_relationship',
                'haart_relationship',
                'trad_med_relationship',
                'comment',
                ]}
         ), audit_fieldset_tuple)
    
    
    radio_fields = {
        'reason_hospitalized': admin.VERTICAL,
        'medical_responsibility': admin.VERTICAL,
        'cause': admin.VERTICAL,
        'cause_category': admin.VERTICAL,
        'perform_autopsy': admin.VERTICAL,
        'participant_hospitalized': admin.VERTICAL,
        'study_drug_relationship': admin.VERTICAL,
        'infant_nvp_relationship': admin.VERTICAL,
        'haart_relationship': admin.VERTICAL,
        'trad_med_relationship': admin.VERTICAL
    }

