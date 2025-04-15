from polls import views
from polls.views import question_list
from django.urls import path

app_name = 'polls'
urlpatterns = [
    path('', question_list, name='question_list'),
    path('register/', views.register_view, name='register'),
]
