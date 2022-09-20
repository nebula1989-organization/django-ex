from django.urls import path

from . import views

urlpatterns = [
    path('', views.news_source_index, name='news_source_index'),

    path('articles/<str:source>', views.list_of_articles, name='list_of_articles'),
]