from django.apps import apps as django_apps
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_visit_schedule import site_visit_schedules

from flourish_prn.models import ChildOffStudy


@receiver(post_save, weak=False, sender=ChildOffStudy,
          dispatch_uid='child_offstudy_on_post_save')
def child_offstudy_on_post_save(sender, instance, raw, created, **kwargs):
    """ Remove fu schedule when child goes offstudy and not already enrolled on
        the followup schedule.
    """
    schedule_history_cls = django_apps.get_model(
        'edc_visit_schedule.subjectschedulehistory')
    participant_note_cls = django_apps.get_model('flourish_calendar.participantnote')
    subject_identifier = instance.subject_identifier
    if not raw:
        fu_notes = participant_note_cls.objects.filter(
            subject_identifier=subject_identifier,
            title='Follow Up Schedule')
        fu_schedule = schedule_history_cls.objects.filter(
            subject_identifier=subject_identifier, schedule_name__contains='_fu')

        if fu_notes.exists() and not fu_schedule.exists():
            fu_notes.delete()
