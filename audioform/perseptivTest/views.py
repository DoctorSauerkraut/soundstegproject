from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .form import AnswerForm, PersonnalInfos, PersonnalInfosForm

def index(request):
    if(request.method == "POST"):
        #Enregistrement des resultats de formulaire
        formPersonnalInfos = PersonnalInfosForm(request.POST).save(True)
        formAnswer  = AnswerForm(request.POST).save(True)
        #redirection
        return redirect('/test')
    else :
        formPersonnalInfos = PersonnalInfosForm()

    formAnswer = AnswerForm()
    template = loader.get_template('index.html')
    i=0
    return render(request,'index.html',{'form':formAnswer, 'formPersoInfo':formPersonnalInfos, 'incr':i, 'dataAnswers':PersonnalInfos.objects.all(), 'sounds':{'audio/sound1.wav','audio/sound2.wav','audio/sound3.wav'}})

# Create your views here.
