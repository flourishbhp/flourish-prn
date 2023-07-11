from ..action_items import MISSED_BIRTH_VISIT_ACTION
from edc_action_item.model_mixins import ActionModelMixin
from edc_base.model_validators import date_not_future,datetime_not_future
from edc_protocol.validators import datetime_not_before_study_start
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO,YES
from edc_base.model_mixins import BaseUuidModel


class MissedBirthVisit(BaseUuidModel,ActionModelMixin):

    tracking_identifier_prefix = 'MB'

    action_name = MISSED_BIRTH_VISIT_ACTION


    report_datetime = models.DateTimeField(
        verbose_name='Report Date',
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        default=get_utcnow,
        help_text=('If reporting today, use today\'s date/time, otherwise use'
                   ' the date/time this information was reported.'))

    infant_dob = models.DateField(
        verbose_name="Date of birth",
        validators=[date_not_future, ],
        null=True,
        blank=True)
    
    weight_avail = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name='Is the infant\'s birth weight available?',
        default=YES,
        help_text="If 'No' go to question 4. Otherwise continue")

    weight_kg = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0),],
        verbose_name="What was the infant's birth weight? ",
        help_text="Measured in Kilograms (kg)",
        blank=True,
        null=True)

    length_avail = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name='Is the infant\'s length at birth available?',
        default=YES,
        help_text="If 'No' go to question 6. Otherwise continue")

    infant_length = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(20), MaxValueValidator(70), ],
        verbose_name="What was the infant's length at birth? ",
        help_text="Measured in centimeters, (cm)",
        blank=True,
        null=True)

    head_circ_avail = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name='Is the infant\'s head circumference at birth available?',
        default=YES,
        help_text="If 'No' go to question 8. Otherwise continue")

    head_circumference = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(11), MaxValueValidator(54)],
        verbose_name="What was the head circumference in centimeters? ",
        help_text="Measured in centimeters, (cm)",
        blank=True,
        null=True)

    gestational_age = models.DecimalField(
        verbose_name="What is the infant's determined gestational age: ",
        max_digits=8,
        decimal_places=2,
        null=True, blank=False)
 
    apgar_score = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Was Apgar Score performed? ",
        help_text="If 'No' go to question 13. Otherwise continue")

    apgar_score_min_1 = models.IntegerField(
        verbose_name="At 1 minute: ",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)])

    apgar_score_min_5 = models.IntegerField(
        verbose_name="At 5 minutes: ",
        blank=True,
        null=True,
        validators=[MaxValueValidator(10),
                    MinValueValidator(0)])

    apgar_score_min_10 = models.IntegerField(
        verbose_name="At 10 minutes: ",
        blank=True,
        null=True,
        validators=[MaxValueValidator(10),
                    MinValueValidator(0)])
    
    congenital_anomalities = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Were any congenital anomalies identified? ",
        help_text="If 'Yes' please complete the Congenital Anomalies below",)
    
    congenital_anomalities_info = models.TextField(
        max_length=255,
        verbose_name="Please add congenital anomalies",
        blank=True,
        null=True,)
    
        
    class Meta:
        app_label = 'flourish_prn'
        verbose_name = 'Missed Birth Visit Form'
        verbose_name_plural = 'Missed Birth Visit Form'