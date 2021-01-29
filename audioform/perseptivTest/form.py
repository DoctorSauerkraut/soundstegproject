from django.forms import ModelForm
from .models import Answers, PersonnalInfos

class AnswerForm(ModelForm):
    class Meta:
        model = Answers
        fields = ['answer']

class PersonnalInfosForm(ModelForm):
    class Meta:
        model = PersonnalInfos
        fields = ['name','email','age','musician']