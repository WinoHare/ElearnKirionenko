from django.contrib import admin

from prof_stats.models import YearsGraph, YearsTable, CitiesGraph, CitiesSalaryTable, CitiesPercentTable, SkillsGraph,\
    SkillsTable, LatestVacancies

admin.site.register(YearsGraph)
admin.site.register(YearsTable)
admin.site.register(CitiesGraph)
admin.site.register(CitiesSalaryTable)
admin.site.register(CitiesPercentTable)
admin.site.register(SkillsGraph)
admin.site.register(SkillsTable)
admin.site.register(LatestVacancies)
