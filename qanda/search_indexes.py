from django.utils import timezone
from haystack import indexes
from .models import Question, Answer, Document
from .templatetags.qanda_tags import textify


# Questions
class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title', boost=1.125)
    title_auto = indexes.EdgeNgramField(model_attr='title')
    model_content = indexes.CharField(model_attr='content')
    answer = indexes.CharField(null=True)
    answered = indexes.BooleanField(model_attr='answered')
    user_email = indexes.CharField(model_attr='user')
    pub_date = indexes.DateTimeField(model_attr='pub_date')
    tags = indexes.MultiValueField(model_attr='tag_list',
                                   faceted=True,
                                   boost=1.5)
    get_absolute_url = indexes.CharField(null=True)

    def get_model(self):
        return Question

    def prepare_get_absolute_url(self, obj):
        return "%s" % obj.get_absolute_url()

    def prepare_user_email(self, obj):
        return "%s" % obj.user_email

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

    def prepare_user_email(self, obj):
        return "%s" % obj.user_email

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=timezone.now())


# Documents
class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    teaser = indexes.CharField(model_attr='teaser')
    title = indexes.CharField(model_attr='title', boost=1.125)
    title_auto = indexes.EdgeNgramField(model_attr='title')
    model_content = indexes.CharField(model_attr='content')
    user_email = indexes.CharField(model_attr='user')
    pub_date = indexes.DateTimeField(model_attr='pub_date')
    updated = indexes.DateTimeField(model_attr='updated')
    tags = indexes.MultiValueField(model_attr='tag_list',
                                   faceted=True,
                                   boost=1.5)
    get_absolute_url = indexes.CharField(null=True)

    def get_model(self):
        return Document

    def prepare_user_email(self, obj):
        return "%s" % obj.user_email

    def prepare_get_absolute_url(self, obj):
        return "%s" % obj.get_absolute_url()

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=timezone.now())
