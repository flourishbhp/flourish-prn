from django.apps import AppConfig as DjangoAppConfig
from django.core.management.color import color_style
from flourish_prn import settings

style = color_style()


class AppConfig(DjangoAppConfig):
    name = 'flourish_prn'
    verbose_name = 'Flourish PRN'
    admin_site_name = 'flourish_prn_admin'


if settings.APP_NAME == 'flourish_prn':
    from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
    from edc_appointment.appointment_config import AppointmentConfig
    from edc_appointment.constants import COMPLETE_APPT
    from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
    from edc_timepoint.apps import AppConfig as BaseEdcTimepointAppConfig
    from edc_timepoint.timepoint import Timepoint
    from edc_timepoint.timepoint_collection import TimepointCollection
    from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig
    from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU

    class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
        default_appt_type = 'clinic'
        configurations = [
            AppointmentConfig(
                model='edc_appointment.appointment',
                related_visit_model='flourish_caregiver.maternalvisit'),
            AppointmentConfig(
                model='flourish_child.appointment',
                related_visit_model='flourish_child.childvisit',
                appt_type='clinic'),
        ]

    class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
        country = 'botswana'
        definitions = {
            '7-day clinic': dict(days=[MO, TU, WE, TH, FR, SA, SU],
                                 slots=[100, 100, 100, 100, 100, 100, 100]),
            '5-day clinic': dict(days=[MO, TU, WE, TH, FR],
                                 slots=[100, 100, 100, 100, 100])}

    class EdcTimepointAppConfig(BaseEdcTimepointAppConfig):
        timepoints = TimepointCollection(
            timepoints=[
                Timepoint(
                    model='edc_appointment.appointment',
                    datetime_field='appt_datetime',
                    status_field='appt_status',
                    closed_status=COMPLETE_APPT),
                Timepoint(
                    model='edc_appointment.historicalappointment',
                    datetime_field='appt_datetime',
                    status_field='appt_status',
                    closed_status=COMPLETE_APPT),
                Timepoint(
                    model='flourish_child.appointment',
                    datetime_field='appt_datetime',
                    status_field='appt_status',
                    closed_status=COMPLETE_APPT),
                Timepoint(
                    model='flourish_child.historicalappointment',
                    datetime_field='appt_datetime',
                    status_field='appt_status',
                    closed_status=COMPLETE_APPT),
            ])

    class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
        visit_models = {
            'flourish_caregiver': (
                'maternal_visit', 'flourish_caregiver.maternalvisit'),
            'flourish_child': (
                'child_visit', 'flourish_child.childvisit')}
