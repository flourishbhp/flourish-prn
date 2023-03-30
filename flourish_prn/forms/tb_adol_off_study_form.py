from django import forms

from flourish_prn.forms import ChildOffStudyForm
from flourish_prn.models import TBAdolOffStudy


class TBAdolOffStudyForm(ChildOffStudyForm, forms.ModelForm):
    class Meta:
        model = TBAdolOffStudy
        fields = '__all__'
