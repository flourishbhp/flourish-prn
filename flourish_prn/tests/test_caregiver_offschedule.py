from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from flourish_caregiver.subject_helper_mixin import SubjectHelperMixin

@tag('os')
class TestCaregiverOffSchedule(TestCase):

    def setUp(self):
        import_holidays()

        self.subject_helper_cls = SubjectHelperMixin()
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
        options = {
            'consent_datetime': get_utcnow() - relativedelta(years=1),
            'version': '3'}

        child_consent_options = {
            'consent_datetime': get_utcnow() - relativedelta(years=1)}

        maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=10, months=1),
            'mom_enrolldate': get_utcnow() - relativedelta(years=10, months=11),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': self.study_maternal_identifier,
            'protocol': 'Tshilo Dikotla',
            'mom_pregarv_strat': '3-drug ART'}

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **maternal_dataset_options)

        child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow() - relativedelta(years=10, months=11),
            'study_maternal_identifier': self.study_maternal_identifier,
            'study_child_identifier': '1143'}

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=10, months=1),
            **child_dataset_options)

        subject_identifier = self.subject_helper_cls.enroll_prior_participant(
            maternal_dataset_obj.screening_identifier,
            child_dataset.study_child_identifier,
            version='3',
            child_version='3',
            options=options,
            child_consent_options=child_consent_options,
            update_created_dt=True)

        onschedule_cls = django_apps.get_model(
            'flourish_caregiver.onschedulecohortbenrollment')
        self.assertEqual(onschedule_cls.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 1)

        mommy.make_recipe(
            'flourish_prn.caregiveroffstudy',
            subject_identifier=subject_identifier,)

        offschedule_cls = django_apps.get_model(
            'flourish_caregiver.caregiveroffschedule')

        self.assertEqual(offschedule_cls.objects.filter(
            subject_identifier=subject_identifier).count(), 1)
