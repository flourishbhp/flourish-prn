from flourish_prn.forms.missed_birth_visit_form import MissedBirthVisitForm
from flourish_prn.models.missed_birth_visit import MissedBirthVisit
from .modeladmin_mixins import ModelAdminMixin
from django.contrib import admin
from ..admin_site import flourish_prn_admin
from edc_model_admin import audit_fieldset_tuple



@admin.register(MissedBirthVisit, site=flourish_prn_admin)
class MissedBirthVisitAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = MissedBirthVisitForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'report_datetime',
                'infant_dob',
                'weight_avail',
                'weight_kg',
                'length_avail',
                'infant_length',
                'head_circ_avail',
                'head_circumference',
                'gestational_age',
                'apgar_score',
                'apgar_score_min_1',
                'apgar_score_min_5',
                'apgar_score_min_10',
                'congenital_anomalities',
                'congenital_anomalities_info')}
         ), audit_fieldset_tuple)


    radio_fields = {
        'apgar_score': admin.VERTICAL,
        'congenital_anomalities': admin.VERTICAL,
        'weight_avail': admin.VERTICAL,
        'length_avail': admin.VERTICAL,
        'head_circ_avail': admin.VERTICAL}