from polls import views
from polls.views import question_list
from . import views
from django.contrib import admin
from django.urls import path, include

app_name = 'polls'
urlpatterns = [
    path('', question_list, name='question_list'),
    path('register/', views.register_view, name='register'),
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
]

