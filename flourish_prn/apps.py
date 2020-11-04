from django.apps import AppConfig as DjangoAppConfig
from django.core.management.color import color_style
from flourish_prn import settings

style = color_style()


class AppConfig(DjangoAppConfig):
    name = 'flourish_prn'
    verbose_name = 'Flourish prn'
    admin_site_name = 'flourish_prn_admin'


if settings.APP_NAME == 'flourish_prn':
    from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
    from edc_appointment.appointment_config import AppointmentConfig

    class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
        default_appt_type = 'clinic'
        configurations = [
            AppointmentConfig(
                model='edc_appointment.appointment',
                related_visit_model='flourish_caregiver.maternalvisit')
        ]
