from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_visit_schedule import site_visit_schedules

from flourish_prn.models import TbReferalAdol


@receiver(post_save, weak=False, sender=TbReferalAdol,
          dispatch_uid='tb_referral_adol_on_post_save')
def tb_referral_adol_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        onschedule_model = 'flourish_child.onscheduletbadolfollowupschedule'
        schedule_name = 'tb_adol_followup_schedule'
        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model, name=schedule_name)

        schedule.put_on_schedule(
            subject_identifier=instance.subject_identifier,
            onschedule_datetime=instance.report_datetime.replace(
                microsecond=0),
            schedule_name=schedule_name,
            base_appt_datetime=instance.report_datetime.replace(
                microsecond=0))
