from django.conf import settings
from django.db import models
from taggit.managers import TaggableManager
from markdownx.models import MarkdownxField
from slugify import slugify

# Create your models here.

# Question
class Question(models.Model):
    """Questions are what they are... or are they?"""
    slug = models.SlugField(max_length=50)
    title = models.CharField(max_length=200, blank=False)
    description = MarkdownxField()
    tags = TaggableManager()
    asked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,)
    asked_on = models.DateTimeField('date published', auto_now_add=True)
    positive_votes = models.IntegerField(default=0)
    negative_votes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

# Answer

# Document

# Comment

# QuestionComment

# AnswerComment

# Tag

# Topic
