from django.db import models

class YearsTable(models.Model):
    """
    Модель со статистикой по годам
    """
    stat = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=100)
    table = models.TextField()
    graph = models.ImageField(upload_to='images/')

class CitiesTable(models.Model):
    """
    Модель со статистикой по городам
    """
    stat = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=150)
    table = models.TextField()
    graph = models.ImageField(upload_to='images/')

class SkillsTable(models.Model):
    """
    Модель со статистикой по навыкам
    """
    year = models.IntegerField()
    table = models.TextField()
    graph = models.ImageField(upload_to='images/')

class Paragraph(models.Model):
    """
    Модель с параграфами для главной страницы
    """
    text_content = models.TextField()
    image = models.ImageField(upload_to='images/')

class ToDo(models.Model):
    """
    Модель с данными по задачам для главной страницы
    """
    name = models.CharField(max_length=150)

class Skill(models.Model):
    """
    Модель с навыками для главной страницы
    """
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images/')


