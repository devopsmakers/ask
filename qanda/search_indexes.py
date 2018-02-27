from django.utils import timezone
from haystack import indexes
from .models import Question, Answer, Document
from .templatetags.qanda_tags import textify


# Questions
class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    answer = indexes.CharField(null=True)
    user = indexes.CharField(model_attr='user')
    pub_date = indexes.DateTimeField(model_attr='pub_date')
    tags = indexes.MultiValueField(model_attr='tag_list')

    def get_model(self):
        return Question

    def prepare_user(self, obj):
        return "%s <%s>" % (obj.user, obj.user.email)

    def prepare_answer(self, obj):
        try:
            return textify(
                "%s" % obj.answer_set.all().filter(accepted=True)[0])
        except IndexError:
            return None

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=timezone.now())


# Answers
class AnswerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr='user')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Answer

    def prepare_user(self, obj):
        return "%s <%s>" % (obj.user, obj.user.email)

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=timezone.now())


# Documents
class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    user = indexes.CharField(model_attr='user')
    pub_date = indexes.DateTimeField(model_attr='pub_date')
    tags = indexes.MultiValueField(model_attr='tag_list')

    def get_model(self):
        return Document

    def prepare_user(self, obj):
        return "%s <%s>" % (obj.user, obj.user.email)

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=timezone.now())
