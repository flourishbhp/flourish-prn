from datetime import date

from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NOT_APPLICABLE
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy


@tag('os')
class TestCaregiverOffSchedule(TestCase):

    def setUp(self):
        import_holidays()

        self.subject_identifier = '12345678'
        self.study_maternal_identifier = '89721'

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=2, months=5),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': self.study_maternal_identifier,
            'protocol': 'Tshilo Dikotla'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': self.study_maternal_identifier,
            'study_child_identifier': '1234'}

    def test_cohort_b_offschedule_valid(self):

        self.subject_identifier = self.subject_identifier[:-1] + '2'
        self.study_maternal_identifier = '981232'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=5,
                                                                                months=2)
        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=1,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=date(2017, 3, 29),
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,
                study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            biological_caregiver=YES,
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier='1234',
            child_dob=(get_utcnow() - relativedelta(years=5, months=4)).date(),)

        mommy.make_recipe(
                    'flourish_caregiver.caregiverpreviouslyenrolled',
                    subject_identifier=subject_consent.subject_identifier)

        onschedule_cls = django_apps.get_model(
            'flourish_caregiver.onschedulecohortbenrollment')
        self.assertEqual(onschedule_cls.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 1)

        mommy.make_recipe(
            'flourish_prn.caregiveroffstudy',
            subject_identifier=subject_consent.subject_identifier,)

        offschedule_cls = django_apps.get_model(
            'flourish_caregiver.caregiveroffschedule')

        self.assertEqual(offschedule_cls.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 1)
