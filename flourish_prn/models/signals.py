from django.apps import apps as django_apps
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_visit_schedule import site_visit_schedules

from flourish_prn.models.child_off_study import ChildOffStudy
from flourish_prn.models.tb_adol_off_study import TBAdolOffStudy


@receiver(post_save, weak=False, sender=ChildOffStudy,
          dispatch_uid='child_offstudy_on_post_save')
def child_offstudy_on_post_save(sender, instance, raw, created, **kwargs):
    """ Remove fu schedule when child goes offstudy and not already enrolled on
        the followup schedule.
    """
    schedule_history_cls = django_apps.get_model(
        'edc_visit_schedule.subjectschedulehistory')
    participant_note_cls = django_apps.get_model(
        'flourish_calendar.participantnote')
    subject_identifier = instance.subject_identifier
    if not raw:
        fu_notes = participant_note_cls.objects.filter(
            subject_identifier=subject_identifier,
            title='Follow Up Schedule')
        fu_schedule = schedule_history_cls.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name__contains='_fu')

        if fu_notes.exists() and not fu_schedule.exists():
            fu_notes.delete()


@receiver(post_save, weak=False, sender=TBAdolOffStudy,
          dispatch_uid='tb_adol_offstudy_post_save')
def tb_adol_offstudy_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        tb_schedules = {
            'tb_adol_schedule': 'flourish_child.onschedulechildtbadolschedule',
            'tb_adol_followup_schedule': 'flourish_child.onscheduletbadolfollowupschedule'
        }
        for schedule_name, onschedule_model in tb_schedules.items():
            _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                onschedule_model=onschedule_model,
                name=schedule_name)
            if schedule.is_onschedule(subject_identifier=instance.subject_identifier,
                                      report_datetime=instance.report_datetime):
                schedule.take_off_schedule(
                    subject_identifier=instance.subject_identifier,
                    schedule_name=schedule_name)
