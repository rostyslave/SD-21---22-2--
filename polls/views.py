from django.shortcuts import render
from .models import Question

def question_list(request):
    """
    Відображення списку всіх питань
    """
    questions = Question.objects.all()
    context = {'questions': questions}
    return render(request, 'question_list.html', context)

