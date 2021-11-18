from edc_action_item import Action, site_action_items, HIGH_PRIORITY

CAREGIVEROFF_STUDY_ACTION = 'submit-caregiveroff-study'
CHILDOFF_STUDY_ACTION = 'submit-childoff-study'
DEATH_REPORT_ACTION = 'submit-death-report'


class CaregiverOffStudyAction(Action):
    name = CAREGIVEROFF_STUDY_ACTION
    display_name = 'Submit Caregiver Offstudy'
    reference_model = 'flourish_prn.caregiveroffstudy'
    admin_site_name = 'flourish_prn_admin'
    priority = HIGH_PRIORITY
    singleton = True


class ChildOffStudyAction(Action):
    name = CHILDOFF_STUDY_ACTION
    display_name = 'Submit Child Offstudy'
    reference_model = 'flourish_prn.childoffstudy'
    admin_site_name = 'flourish_prn_admin'
    priority = HIGH_PRIORITY
    singleton = True


class CaregiverDeathReportAction(Action):
    name = DEATH_REPORT_ACTION
    display_name = 'Submit Caregiver Death Report'
    reference_model = 'flourish_prn.deathreport'
    admin_site_name = 'flourish_prn_admin'
    priority = HIGH_PRIORITY
    singleton = True


site_action_items.register(CaregiverOffStudyAction)
site_action_items.register(ChildOffStudyAction)
site_action_items.register(CaregiverDeathReportAction)

