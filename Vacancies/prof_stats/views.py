from django.shortcuts import render
from django.http import JsonResponse
from prof_stats.models import *
from prof_stats.HHRequests import HHRequests

def index(request):
    """
    Возвращает главную страницу

    Args:
        request: Отправленный запрос
    """
    paragraphs = Paragraph.objects.all()
    first_paragraph = paragraphs[0]
    second_paragraph = paragraphs[1]
    ToDos = ToDo.objects.all()
    Skills = Skill.objects.all()
    return render(request, "index.html", {'first_paragraph': first_paragraph, 'second_paragraph': second_paragraph,
                                          'ToDos': ToDos, 'skills': Skills})

def demand(request):
    """
    Возвращает страницу со статистиками по годам

    Args:
        request: Отправленный запрос
    """
    demands = YearsTable.objects.all()
    return render(request, "demand.html", {"demands": demands})

def geography(request):
    """
    Возвращает страницу со статистиками по городам

    Args:
        request: Отправленный запрос
    """
    cities = CitiesTable.objects.all()
    return render(request, "geography.html", {"cities": cities})

def skills(request):
    """
    Возвращает страницу со статистиками по навыкам

    Args:
        request: Отправленный запрос
    """
    table = SkillsTable.objects.all()
    return render(request, "skills.html", {"skills": table})

def latest_vacancies(request):
    """
    Возвращает страницу с последними вакансиями

    Args:
        request: Отправленный запрос
    """
    return render(request, "latest-vacancies.html")

def get_vacancies(request):
    """
    Возвращает JSON с вакансиями с HH.ru

    Args:
        request: Отправленный запрос
    """
    day = request.GET.get('day')
    vacancies = HHRequests().upload_vacancies_by_day(day)
    return JsonResponse({'items': vacancies})
