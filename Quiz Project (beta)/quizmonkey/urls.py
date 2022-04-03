from django.urls import path
from quizmonkey import views

urlpatterns = [
    path('', views.front_page, name='front_page'),

    path('main-page', views.main_page, name='main-page'),
    path('questionnaire/<int:questionnaire_id>/', views.get_questionnaire, name='get_questionnaire'),
    path('vote', views.submit_vote, name='vote'),
    path('index', views.index, name='index'),
]