from django.conf import settings
from django.db import models
from django.utils import timezone

class YearsGraph(models.Model):
    stat = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/images/')

class YearsTable(models.Model):
    year = models.IntegerField(primary_key=True)
    salary = models.IntegerField()
    prof_salary = models.IntegerField()
    count = models.IntegerField()
    prof_count = models.IntegerField()

class CitiesGraph(models.Model):
    stat = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/images/')

class CitiesSalaryTable(models.Model):
    city = models.CharField(max_length=30)
    salary = models.IntegerField()

class CitiesPercentTable(models.Model):
    city = models.CharField(max_length=30)
    percent = models.FloatField()

class SkillsGraph(models.Model):
    stat = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/images/')

class SkillsTable(models.Model):
    skill = models.CharField(max_length=30)
    count = models.IntegerField()

class LatestVacancies(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.TextField()
    company = models.CharField(max_length=100)
    salary = models.IntegerField()
    area_name = models.CharField(max_length=100)
    published_at = models.DateTimeField()
    url = models.URLField()
