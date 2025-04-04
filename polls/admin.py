from django.contrib import admin

from polls.models import Question, Choice

@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Choice)
class ChoiceModelAdmin(admin.ModelAdmin):
    pass

# Register your models here.
