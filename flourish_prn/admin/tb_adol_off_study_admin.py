from django.contrib import admin

from flourish_prn.admin import ChildOffStudyAdmin
from flourish_prn.admin_site import flourish_prn_admin
from flourish_prn.forms import TBAdolOffStudyForm
from flourish_prn.models import TBAdolOffStudy


@admin.register(TBAdolOffStudy, site=flourish_prn_admin)
class TBAdolOffStudyAdmin(ChildOffStudyAdmin, admin.ModelAdmin):
    form = TBAdolOffStudyForm
