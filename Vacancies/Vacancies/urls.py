from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from prof_stats import views

#Маршрутизация

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index),
    path('geography/', views.geography),
    path('demand/', views.demand),
    path('skills/', views.skills),
    path('latest_vacancies/', views.latest_vacancies),
    path('vacancies/', views.get_vacancies)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
