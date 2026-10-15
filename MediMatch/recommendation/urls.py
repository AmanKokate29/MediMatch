from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recommend/', views.recommend, name='recommend'),
    path('results/', views.results, name='results'),
    path('history/', views.history, name='history'),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
    path('nearby/', views.nearby, name='nearby'),
]
