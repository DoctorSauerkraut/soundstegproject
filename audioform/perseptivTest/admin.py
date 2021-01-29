from django.contrib import admin
from .models import Answers, AnswersAdmin, PersonnalInfos
# Register your models here.
admin.site.register(PersonnalInfos, AnswersAdmin)
