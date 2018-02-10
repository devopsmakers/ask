from django.contrib import admin
from .models import Question
from markdownx.admin import MarkdownxModelAdmin

# Register your models here

@admin.register(Question)
class QuestionAdmin(MarkdownxModelAdmin):
    pass
