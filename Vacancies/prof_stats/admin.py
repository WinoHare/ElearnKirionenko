from django.contrib import admin
from prof_stats.models import *

# Добавление в админку моделей

admin.site.register(YearsTable)
admin.site.register(CitiesTable)
admin.site.register(SkillsTable)
admin.site.register(Paragraph)
admin.site.register(ToDo)
admin.site.register(Skill)
