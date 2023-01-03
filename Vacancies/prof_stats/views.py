import datetime
from django.http import HttpResponse
from django.shortcuts import render
from prof_stats.models import *
from processing.InputConnect import InputConnect
from processing.HHRequests import HHRequests

last_unloading_date = datetime.datetime.now()
# Create your views here.

def index(request):
    return render(request, "index.html")

def demand(request):
    graphs = YearsGraph.objects.all()
    table = YearsTable.objects.all()
    return render(request, "demand.html", {"graphs": graphs, "table": table})

def geography(request):
    graphs = CitiesGraph.objects.all()
    salary_table  = CitiesSalaryTable.objects.all()
    percent_table = CitiesPercentTable.objects.all()
    return render(request, "geography.html", {"graphs": graphs, "salary_table": salary_table,
                                              "percent_table": percent_table})

def skills(request):
    graphs = SkillsGraph.objects.all()
    table = SkillsTable.objects.all()
    return render(request, "skills.html", {"graphs": graphs, "table": table})

def latest_vacancies(request):
    vacancies = LatestVacancies.objects.all()
    if len(vacancies) == 0:
        HHRequests()
        vacancies = LatestVacancies.objects.all()
    elif vacancies[0].published_at.day < datetime.datetime.now().day - 2:
        HHRequests()
        vacancies = LatestVacancies.objects.all()

    return render(request, "latest-vacancies.html", {"vacancies": vacancies})

def processing(request):
    InputConnect()
    return HttpResponse("Сделано")