from django.db.models import (FileField, ForeignKey, ImageField, ManyToManyField,
                              ManyToOneRel, OneToOneField)
from django.db.models.fields.reverse_related import OneToOneRel
from django.utils.translation import ugettext_lazy as _
from django.apps import apps as django_apps

from flourish_export.admin_export_helper import AdminExportHelper


class ExportActionMixin(AdminExportHelper):

    def update_variables(self, subject_identifier, data={}):
        """ Update study identifiers to desired variable name(s).
        """
        new_data_dict = {}
        replace_idx = {'child_subject_identifier': 'childpid',
                       'study_maternal_identifier': 'old_matpid',
                       'study_child_identifier': 'old_childpid'}

        if len(subject_identifier.split('-')) == 3:
            replace_idx.update(
                {'subject_identifier': 'matpid'})
        elif len(subject_identifier.split('-')) == 4:
            replace_idx.update(
                {'subject_identifier': 'childpid'})

        for old_idx, new_idx in replace_idx.items():
            try:
                new_data_dict[new_idx] = data.pop(old_idx)
            except KeyError:
                continue
        new_data_dict.update(data)
        return new_data_dict

    def export_as_csv(self, request, queryset):
        records = []

        for obj in queryset:
            data = obj.__dict__.copy()
            subject_identifier = getattr(obj, 'subject_identifier', None)

            dob = self.dob_obj(subject_identifier)

            if dob:
                data.update(dob=dob.strftime('%Y/%m/%d'))
            else:
                data.update(dob='N/A')

            # Update variable names for study identifiers
            data = self.update_variables(subject_identifier, data)

            for field in self.get_model_fields:
                field_name = field.name
                if isinstance(field, (ForeignKey, OneToOneField, OneToOneRel,)):
                    continue
                if isinstance(field, (FileField, ImageField,)):
                    file_obj = getattr(obj, field_name, '')
                    data.update({f'{field_name}': getattr(file_obj, 'name', '')})
                    continue
                if isinstance(field, ManyToManyField):
                    data.update(self.m2m_data_dict(obj, field))
                    continue
                if isinstance(field, ManyToOneRel):
                    data.update(self.inline_data_dict(obj, field))
                    continue

            # Exclude identifying values
            data = self.remove_exclude_fields(data)
            # Correct date formats
            data = self.fix_date_formats(data)
            records.append(data)

        response = self.write_to_csv(records)
        return response

    export_as_csv.short_description = _(
        'Export selected %(verbose_name_plural)s')

    actions = [export_as_csv]

    def dob_obj(self, subject_identifier: str):
        consent_cls = django_apps.get_model(
            'flourish_caregiver.subjectconsent')
        child_consent_cls = django_apps.get_model(
            'flourish_caregiver.caregiverchildconsent')

        query_attr = {'subject_identifier': subject_identifier}
        caregiver_dob = getattr(
            self.get_model_obj(consent_cls, query_attr), 'dob', None)

        child_dob = getattr(
            self.get_model_obj(child_consent_cls, query_attr), 'child_dob', None)

        return caregiver_dob or child_dob

    def get_model_obj(self, model_cls, query_attrs={}):
        try:
            return model_cls.objects.filter(
                **query_attrs).latest('consent_datetime')
        except model_cls.DoesNotExist:
            return None

    @property
    def exclude_fields(self):
        return ['_state', 'hostname_created', 'hostname_modified',
                'revision', 'device_created', 'device_modified', 'id',
                'site_id', 'modified_time', 'report_datetime_time',
                'registration_datetime_time', 'screening_datetime_time',
                'modified', 'form_as_json', 'consent_model',
                'randomization_datetime', 'registration_datetime',
                'is_verified_datetime', 'first_name', 'last_name', 'initials',
                'guardian_name', 'identity', 'related_tracking_identifier',
                'parent_tracking_identifier', 'action_identifier',
                'tracking_identifier', 'slug', 'confirm_identity', 'site',
                'subject_consent_id', '_django_version', ]
