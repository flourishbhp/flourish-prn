from django import forms
from django.apps import apps as django_apps
from django.db import models
from edc_base.model_fields.custom_fields import OtherCharField
from edc_base.model_validators import date_not_future, datetime_not_future
from edc_base.utils import get_utcnow
from edc_protocol.validators import date_not_before_study_start, datetime_not_before_study_start
from flourish_child.helper_classes.utils import child_utils

from ..choices import COMMUNICATION_METHODS


class OffStudyModelMixin(models.Model):

    offstudy_date = models.DateField(
        verbose_name="Off-study Date",
        validators=[
            date_not_before_study_start,
            date_not_future])

    reason_other = OtherCharField()

    results_method = models.CharField(
        verbose_name=('Methods used to communicate study findings'
                      ' to the participant'),
        max_length=20,
        choices=COMMUNICATION_METHODS)

    results_dt = models.DateTimeField(
        verbose_name='Date and time findings communicated',
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        null=True,
        blank=True)

    comment = models.TextField(
        max_length=250,
        verbose_name="Comment",
        blank=True,
        null=True)

    def get_consent_version(self):
        preg_subject_screening_cls = django_apps.get_model(
            'flourish_caregiver.screeningpregwomen')
        prior_subject_screening_cls = django_apps.get_model(
            'flourish_caregiver.screeningpriorbhpparticipants')

        consent_version_cls = django_apps.get_model(
            'flourish_caregiver.flourishconsentversion')

        subject_screening_obj = None
        subject_identifier = self.subject_identifier
        if len(self.subject_identifier.split('-')) == 4:
            subject_identifier = child_utils.caregiver_subject_identifier(
                self.subject_identifier)

        try:
            subject_screening_obj = preg_subject_screening_cls.objects.get(
                subject_identifier=subject_identifier)
        except preg_subject_screening_cls.DoesNotExist:
            try:
                subject_screening_obj = prior_subject_screening_cls.objects.get(
                    subject_identifier=subject_identifier)
            except prior_subject_screening_cls.DoesNotExist:
                raise forms.ValidationError(
                    'Missing Subject Screening form. Please complete '
                    'it before proceeding.')

        if subject_screening_obj:
            try:
                consent_version_obj = consent_version_cls.objects.get(
                    screening_identifier=subject_screening_obj.screening_identifier)
            except consent_version_cls.DoesNotExist:
                raise forms.ValidationError(
                    'Missing Consent Version form. Please complete '
                    'it before proceeding.')
            return consent_version_obj.version

    def save(self, *args, **kwargs):
        self.consent_version = self.get_consent_version()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
