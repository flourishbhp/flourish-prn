from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_action_item import Action, site_action_items, HIGH_PRIORITY

CAREGIVEROFF_STUDY_ACTION = 'submit-caregiveroff-study'
CHILDOFF_STUDY_ACTION = 'submit-childoff-study'
CAREGIVER_DEATH_REPORT_ACTION = 'submit-caregiver-death-report'
CHILD_DEATH_REPORT_ACTION = 'submit-child-death-report'


class CaregiverOffStudyAction(Action):
    name = CAREGIVEROFF_STUDY_ACTION
    display_name = 'Submit Caregiver Offstudy'
    reference_model = 'flourish_prn.caregiveroffstudy'
    admin_site_name = 'flourish_prn_admin'
    show_link_to_add = True
    priority = HIGH_PRIORITY
    singleton = True


class ChildOffStudyAction(Action):
    name = CHILDOFF_STUDY_ACTION
    display_name = 'Submit Child Offstudy'
    reference_model = 'flourish_prn.childoffstudy'
    admin_site_name = 'flourish_prn_admin'
    show_link_to_add = True
    priority = HIGH_PRIORITY
    singleton = True

    def get_next_actions(self):
        actions = []
        offstudy = None
        child_deathreport_cls = django_apps.get_model(
            'flourish_prn.childdeathreport')

        action_item_cls = django_apps.get_model(
            'edc_action_item.actionitem')

        subject_identifier = self.reference_model_obj.subject_identifier
        offstudy = action_item_cls.objects.filter(
            subject_identifier=subject_identifier,
            action_type__name=CHILD_DEATH_REPORT_ACTION)
        try:
            child_deathreport_cls.objects.get(
                subject_identifier=subject_identifier)
            if not offstudy:
                actions = [ChildOffStudyAction]
        except ObjectDoesNotExist:
            pass
        return actions


class CaregiverDeathReportAction(Action):
    name = CAREGIVER_DEATH_REPORT_ACTION
    display_name = 'Submit Caregiver Death Report'
    reference_model = 'flourish_prn.caregiverdeathreport'
    admin_site_name = 'flourish_prn_admin'
    show_link_to_add = True
    priority = HIGH_PRIORITY
    singleton = True

    def get_next_actions(self):
        actions = []
        offstudy = None
        caregiver_deathreport_cls = django_apps.get_model(
            'flourish_prn.caregiverdeathreport')

        action_item_cls = django_apps.get_model(
            'edc_action_item.actionitem')

        subject_identifier = self.reference_model_obj.subject_identifier
        offstudy = action_item_cls.objects.filter(
            subject_identifier=subject_identifier,
            action_type__name=CAREGIVEROFF_STUDY_ACTION)
        try:
            caregiver_deathreport_cls.objects.get(
                subject_identifier=subject_identifier)
            if not offstudy:
                actions = [CaregiverOffStudyAction]
        except ObjectDoesNotExist:
            pass
        return actions


class ChildDeathReportAction(Action):
    name = CHILD_DEATH_REPORT_ACTION
    display_name = 'Submit Child Death Report'
    reference_model = 'flourish_prn.childdeathreport'
    admin_site_name = 'flourish_prn_admin'
    show_link_to_add = True
    priority = HIGH_PRIORITY
    singleton = True


site_action_items.register(CaregiverOffStudyAction)
site_action_items.register(ChildOffStudyAction)
site_action_items.register(CaregiverDeathReportAction)
site_action_items.register(ChildDeathReportAction)
