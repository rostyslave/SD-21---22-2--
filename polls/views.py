from django.shortcuts import render

from .Forms import UserRegistrationForm, UserLoginForm
from .models import Question

def question_list(request):
    """
    Відображення списку всіх питань
    """
    questions = Question.objects.all()
    context = {'questions': questions}
    return render(request, 'question_list.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth import login


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('polls:question_list')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {"form": form})


from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Ласкаво просимо, {username}!")
                return redirect('home')
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Ви успішно вийшли з системи!")
    return redirect('login')
