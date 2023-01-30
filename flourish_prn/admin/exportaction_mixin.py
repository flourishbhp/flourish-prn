import datetime
import uuid

from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import xlwt
from django.apps import apps as django_apps

class ExportActionMixin:

    def export_as_csv(self, request, queryset):

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % (
            self.get_export_filename())

        wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
        ws = wb.add_sheet('%s')

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.num_format_str = 'YYYY/MM/DD h:mm:ss'

        field_names = queryset[0].__dict__
        field_names = [a for a in field_names.keys()]
        field_names.remove('_state')
        field_names.append('dob')


        for col_num in range(len(field_names)):
            ws.write(row_num, col_num, field_names[col_num], font_style)

        for obj in queryset:
            obj_data = obj.__dict__
            
            dob = self.dob_obj(obj_data['subject_identifier'])
            
            if dob:
                obj_data['dob'] = self.dob_obj(obj_data['subject_identifier']).strftime('%Y/%m/%d')
            else:
                obj_data['dob'] = 'N/A'
            
            data = [obj_data[field] for field in field_names]

            row_num += 1
            for col_num in range(len(data)):
                
                if isinstance(data[col_num], uuid.UUID):
                    ws.write(row_num, col_num, str(data[col_num]))
                elif isinstance(data[col_num], datetime.datetime):
                    data[col_num] = timezone.make_naive(data[col_num])
                    ws.write(row_num, col_num, data[col_num], xlwt.easyxf(num_format_str='YYYY/MM/DD h:mm:ss'))
                else:
                    ws.write(row_num, col_num, data[col_num])
        wb.save(response)
        return response

    export_as_csv.short_description = _(
        'Export selected %(verbose_name_plural)s')

    actions = [export_as_csv]
    
    def dob_obj(self, subject_identifier: str):
        consent_cls = django_apps.get_model('flourish_caregiver.subjectconsent')
        child_consent_cls = django_apps.get_model('flourish_caregiver.caregiverchildconsent')
         
        try:
            consent = consent_cls.objects.filter(
                subject_identifier=subject_identifier).latest('consent_datetime')
        except consent_cls.DoesNotExist:
            consent = child_consent_cls.objects.filter(
                subject_identifier=subject_identifier).latest('consent_datetime')
            return consent.child_dob
        else:
            return consent.dob

    def get_export_filename(self):
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        filename = "%s-%s" % (self.model.__name__, date_str)
        return filename
