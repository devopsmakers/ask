from django.conf import settings
from django.db import models
from taggit.managers import TaggableManager
from markdownx.models import MarkdownxField
from slugify import slugify
import reversion

# Create your models here.

# Question
class QuestionManager(models.Manager):
    use_for_related_models = True

    def answered(self, **kwargs):
        return self.filter(answered=True, **kwargs)

    def unanswered(self, **kwargs):
        return self.filter(answered=False, **kwargs)

class Question(models.Model):
    """Questions are what they are... or are they?"""
    slug = models.SlugField(max_length=50, blank=True)
    title = models.CharField(max_length=200, blank=False)
    content = MarkdownxField(blank=True, null=True)
    tags = TaggableManager(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    positive_votes = models.IntegerField(default=0)
    negative_votes = models.IntegerField(default=0)
    answered = models.BooleanField(default=False)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)


# Answer
class Answer(models.Model):
    """Answers belong to a question."""
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )
    content = MarkdownxField();
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    updated = models.DateTimeField('date updated', auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    accepted = models.BooleanField(default=False)
    positive_votes = models.IntegerField(default=0)
    negative_votes = models.IntegerField(default=0)

    def __str__(self):  # pragma: no cover
        return self.content

    class Meta:
        ordering = ['-accepted', '-pub_date']


# Topic
class Topic(models.Model):
    slug = models.SlugField(max_length=50, blank=True)
    title = models.CharField(max_length=200, blank=False)
    tags = TaggableManager(blank=True)

    def __str__(self):  # pragma: no cover
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Topic, self).save(*args, **kwargs)


# Document
@reversion.register()
class Document(models.Model):
    """A business document such as a policy or official process"""
    slug = models.SlugField(max_length=50, blank=True)
    title = models.CharField(max_length=200, blank=False)
    content = MarkdownxField()
    tags = TaggableManager(blank=True)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    updated = models.DateTimeField('date updated', auto_now=True)
    positive_votes = models.IntegerField(default=0)
    negative_votes = models.IntegerField(default=0)

    def __str__(self):  # pragma: no cover
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Document, self).save(*args, **kwargs)


# Vote
class Vote(models.Model):
    """Abstract model that other votes come from"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    value = models.BooleanField(default=True)

    class Meta:
        abstract = True


# QuestionVote
class QuestionVote(Vote):
    """Users can vote on questions"""
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (('user', 'question'),)


# AnswerVote
class AnswerVote(Vote):
    """Users can vote on answers"""
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (('user', 'answer'),)


# DocumentVote
class DocumentVote(Vote):
    """Users can vote on documents"""
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (('user', 'document'),)


# Comment
class Comment(models.Model):
    """abstract model that other comments come from"""
    content = MarkdownxField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def __str__(self):  # pragma: no cover
        return self.content


# QuestionComment
class QuestionComment(Comment):
    """Comments on questions"""
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )


# AnswerComment
class AnswerComment(Comment):
    """Comments on answers"""
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
    )

# DocumentComment
class DocumentComment(Comment):
    """Comments on documents"""
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
    )
