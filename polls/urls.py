from polls.views import question_list
from django.urls import path

app_name = 'polls'
urlpatterns = [
    path('', question_list, name='question_list'),
]
