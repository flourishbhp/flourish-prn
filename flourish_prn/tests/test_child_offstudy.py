from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from flourish_caregiver.subject_helper_mixin import SubjectHelperMixin

@tag('cos')
class TestChildOffStudy(TestCase):

    def setUp(self):
        import_holidays()

        self.subject_helper_cls = SubjectHelperMixin()
        self.study_maternal_identifier = '981232'

        self.options = {
            'consent_datetime': get_utcnow() - relativedelta(years=1),
            'version': '3'}

        self.child_consent_options = {
            'consent_datetime': get_utcnow() - relativedelta(years=1)}

        maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=10, months=1),
            'mom_enrolldate': get_utcnow() - relativedelta(years=10, months=11),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': self.study_maternal_identifier,
            'protocol': 'Tshilo Dikotla',
            'mom_pregarv_strat': '3-drug ART'}

        self.maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **maternal_dataset_options)

        child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow() - relativedelta(years=4, months=11),
            'study_maternal_identifier': self.study_maternal_identifier,
            'study_child_identifier': '1234'}

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=4, months=1),
            **child_dataset_options)

        self.subject_identifier = self.subject_helper_cls.enroll_prior_participant(
            self.maternal_dataset_obj.screening_identifier,
            child_dataset.study_child_identifier,
            version='3',
            child_version='3',
            options=self.options,
            child_consent_options=self.child_consent_options,
            update_created_dt=True)

    def test_caregiver_offschedule_valid(self):

        onschedule_cls = django_apps.get_model(
            'flourish_caregiver.onschedulecohortaenrollment')

        # Check first child enrolled onschedule
        onschedule = onschedule_cls.objects.filter(
            subject_identifier=self.subject_identifier,
            schedule_name='a_enrol1_schedule1',)
        self.assertEqual(onschedule.count(), 1)
        first_child_schedules = [onschedule[0].schedule_name]

        child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow() - relativedelta(years=10, months=11),
            'study_maternal_identifier': self.study_maternal_identifier,
            'study_child_identifier': '1143'}

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=10, months=1),
            **child_dataset_options)

        consent_cls = django_apps.get_model(
            'flourish_caregiver.subjectconsent')
        subject_consent = consent_cls.objects.get(
            subject_identifier=self.subject_identifier)
    
        child_consent = mommy.make_recipe(
                'flourish_caregiver.caregiverchildconsent',
                subject_consent=subject_consent,
                study_child_identifier=child_dataset.study_child_identifier,
                child_dob=self.maternal_dataset_obj.delivdt,
                **self.child_consent_options)
        subject_consent.save()
        child_consent.save()

        onschedule_cls = django_apps.get_model(
            'flourish_caregiver.onschedulecohortbenrollment')

        # Check second child enrolled onschedule
        onschedule = onschedule_cls.objects.filter(
            subject_identifier=self.subject_identifier,
            child_subject_identifier=child_consent.subject_identifier,)
        self.assertEqual(onschedule.count(), 1)

        appointment_cls = django_apps.get_model(
            'edc_appointment.appointment')
        appointment = appointment_cls.objects.filter(
            subject_identifier=self.subject_identifier,
            schedule_name=onschedule[0].schedule_name)

        # Enrol second child to the quarterly schedule
        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=appointment[0],
            subject_identifier=self.subject_identifier)

        quart_onschedule_cls = django_apps.get_model(
            'flourish_caregiver.onschedulecohortbquarterly')
        quart_onschedule = quart_onschedule_cls.objects.filter(
            subject_identifier=self.subject_identifier,
            child_subject_identifier=child_consent.subject_identifier,)
        self.assertEqual(quart_onschedule.count(), 1)

        second_child_schedules = [onschedule[0].schedule_name,
                                  quart_onschedule[0].schedule_name]
        # Take second child offstudy
        mommy.make_recipe(
            'flourish_prn.childoffstudy',
            subject_identifier=child_consent.subject_identifier,)

        # Check caregiver taken offschedule for second child schedules
        offschedule_cls = django_apps.get_model(
            'flourish_caregiver.caregiveroffschedule')     
        offschedule_objs = offschedule_cls.objects.filter(
            subject_identifier=self.subject_identifier)
        self.assertEqual(offschedule_objs.count(), 2)
        self.assertListEqual(
            list(offschedule_objs.values_list('schedule_name', flat=True)),
            second_child_schedules)

        self.assertTrue(len(first_child_schedules), 0)
