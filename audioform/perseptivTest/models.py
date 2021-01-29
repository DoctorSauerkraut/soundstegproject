from django.db import models
from django.contrib import admin

# Create your models here.
class Answers(models.Model):
    answer = models.CharField(max_length=150,default="")

class PersonnalInfos(models.Model):
    name = models.CharField(max_length=25, default="")
    age = models.IntegerField(default=20)
    email = models.EmailField(max_length=45,default="")
    musician = models.BooleanField(default=False)


class AnswersAdmin(admin.ModelAdmin):
    list_display = ("name","email","musician")
    list_filter = ("name",)
    search_fields = ["name", "answer"]