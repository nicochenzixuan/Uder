from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('welcome/', views.welcome, name = 'welcome'),  
    #path('<str:username>/welcome/', views.welcome, name = 'welcome'),
    path('welcome/driver', views.driver, name = 'driver'),
    #path('<int:question_id>/vote/', views.vote, name='vote'),
]

