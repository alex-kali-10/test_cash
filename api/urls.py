from django.urls import include, path
from rest_framework import routers
from . import views


urlpatterns = [
    path('article_list/', views.article_list),
    path('article/<int:pk>', views.article),
]