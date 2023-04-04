from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_prn_admin
from ..forms import TbReferralAdolForm
from ..models import TbReferalAdol

from .modeladmin_mixins import ModelAdminMixin


@admin.register(TbReferalAdol, site=flourish_prn_admin)
class TbReferralAdolAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = TbReferralAdolForm

    search_fields = ('subject_identifier',)

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                'referral_date',
                'location',
                'location_other']}
         ), audit_fieldset_tuple)

    radio_fields = {'location': admin.VERTICAL, }
