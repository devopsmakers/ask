from django.contrib import admin
from .models import Question, QuestionVote, QuestionComment
from .models import Answer, AnswerVote, AnswerComment
from .models import Document, DocumentVote, DocumentComment, Topic
from markdownx.admin import MarkdownxModelAdmin
from reversion.admin import VersionAdmin


# Register your models here

# Question related admin stuff
class QuestionVoteInline(admin.TabularInline):
    model = QuestionVote


class QuestionCommentInline(admin.TabularInline):
    model = QuestionComment


@admin.register(Question)
class QuestionAdmin(MarkdownxModelAdmin):
    inlines = [
        QuestionVoteInline,
        QuestionCommentInline,
    ]


# Answer related admin stuff
class AnswerVoteInline(admin.TabularInline):
    model = AnswerVote


class AnswerCommentInline(admin.TabularInline):
    model = AnswerComment


@admin.register(Answer)
class AnswerAdmin(MarkdownxModelAdmin):
    filter_horizontal = ('documents',)
    inlines = [
        AnswerVoteInline,
        AnswerCommentInline,
    ]


# Document related admin stuff
class DocumentVoteInline(admin.TabularInline):
    model = DocumentVote


class DocumentCommentInline(admin.TabularInline):
    model = DocumentComment


@admin.register(Document)
class DocumentAdmin(MarkdownxModelAdmin, VersionAdmin):
    inlines = [
        DocumentVoteInline,
        DocumentCommentInline,
    ]


# Topic related admin stuff
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass
