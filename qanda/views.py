import logging

from django.db.models import F
from django.shortcuts import render
from django.views.generic import FormView, View, CreateView, DetailView, \
    ListView, TemplateView, UpdateView
from django.conf import settings
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.http.response import HttpResponseRedirect

from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet, SQ
from haystack.inputs import AutoQuery, Exact, Clean, Raw

from .forms import QuestionForm, DocumentForm, EmptySearchForm, AnswerForm
from .models import Question, QuestionManager, Document, Answer
from .utils import strip_stop_words

logger = logging.getLogger(__name__)

try:
    qanda_messages = 'django.contrib.messages' in settings.INSTALLED_APPS and \
        settings.ORG_SETTINGS['messages']

except AttributeError:  # pragma: no cover
    qanda_messages = False

if qanda_messages:
    from django.contrib import messages

# QandaBaseView
class QandaBaseView(View):
    def get_context_data(self, **kwargs):
        context = super(QandaBaseView, self).get_context_data(**kwargs)
        context['ORGANIZATION_NAME'] = settings.ORG_SETTINGS.get(
            'organization', '')
        context['LOGO'] = settings.ORG_SETTINGS.get(
            'logo', False)
        context['unanswered_count'] = Question.objects.unanswered().count()
        return context


# IndexView
class IndexView(QandaBaseView, TemplateView):
    """ Home / index view """
    template_name = 'qanda/index.html'

    def voted_documents(self):
        return Document.objects.order_by(
            (F('positive_votes') - F('negative_votes')).desc()).select_related('user')[:5]

    def newest_questions(self):
        return Question.objects.order_by('-pub_date').select_related('user')[:5]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['nav'] = 'search'
        return context


# SearchView
class SearchResultsView(QandaBaseView, SearchView):
    """ Search results view """
    template_name = 'qanda/results.html'
    context_object_name = 'questions_list'
    form_class = EmptySearchForm

    def get_queryset(self):
        queryset = super(SearchResultsView, self).get_queryset()
        search_string = str(Clean(self.request.GET.get('q', '')))
        key_words = strip_stop_words(search_string)

        queryset = queryset.filter(django_ct=Exact('qanda.question'))
        if len(key_words) > 1:
            queryset = queryset.filter(
               SQ(text__contains=search_string) | SQ(text__contains=key_words) |
               SQ(tags__in=key_words.split())
            )
        else:
            queryset = queryset.filter(
               SQ(text__contains=search_string)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        search_string = str(Clean(self.request.GET.get('q', '')))
        key_words = strip_stop_words(search_string)

        document_qs = SearchQuerySet().filter(django_ct=Exact('qanda.document'))
        if len(key_words) > 1:
            document_qs = document_qs.filter(
               SQ(text__contains=search_string) | SQ(text__contains=key_words) |
               SQ(tags__in=key_words.split())
            )[:5]
        else:
            document_qs = document_qs.filter(
               SQ(text__contains=search_string)
            )[:5]
        context['documents_list'] = document_qs
        context['nav'] = 'search'
        return context


# HelpView
class HelpView(QandaBaseView, TemplateView):
    """ Help view """
    template_name = 'qanda/help.html'

    def get_context_data(self, **kwargs):
        context = super(HelpView, self).get_context_data(**kwargs)
        context['nav'] = 'help'
        return context

# UnansweredView
class UnansweredView(QandaBaseView, ListView):
    """ Unanswered questions view """
    template_name = 'qanda/results.html'
    model = Question
    queryset = Question.objects.unanswered().order_by('pub_date')
    context_object_name = "questions_list"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(UnansweredView, self).get_context_data(**kwargs)
        context['nav'] = 'unanswered'
        return context


# QuestionView
class QuestionView(QandaBaseView, DetailView, CreateView):
    model = Question
    message = _('Thank you! Your answer has been created.')
    template_name = 'qanda/detail.html'
    form_class = AnswerForm


    def html_content(self):
        return self.object.html_content

    def get_queryset(self):
        queryset = super(QuestionView, self).get_queryset()
        return queryset.prefetch_related('answer_set').prefetch_related(
            'answer_set__documents',
            'answer_set__user')

    def form_valid(self, form):
        """
        Create the required relation
        """
        form.instance.user = self.request.user
        form.instance.question = self.get_object()
        return super().form_valid(form)

    def get(self, request, **kwargs):
        self.object = self.get_object()
        if self.request.path != self.object.get_absolute_url():
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

    def get_success_url(self):
        if qanda_messages:
            messages.success(self.request, self.message)
        question = self.get_object()
        return reverse('qanda_question_view',
                       kwargs={'pk': question.pk, 'slug': question.slug})

# AskQuestionView
class AskQuestionView(QandaBaseView, CreateView):
    """
    Create a question
    """
    template_name = 'qanda/create_form.html'
    message = _('Thank you! Your question has been created.')
    form_class = QuestionForm

    def form_valid(self, form):
        """
        Create the required relation
        """
        form.instance.user = self.request.user
        return super(AskQuestionView, self).form_valid(form)

    def get_success_url(self):
        if qanda_messages:
            messages.success(self.request, self.message)
        return reverse('qanda_index')

# UpdateQuestionView
class UpdateQuestionView(QandaBaseView, UpdateView):
    """
    Update a question
    """
    template_name = 'qanda/update_form.html'
    message = _('Thank you! your question has been updated.')
    form_class = QuestionForm
    model = Question
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        """
        Create the required relation
        """
        form.instance.user = self.request.user
        return super(UpdateQuestionView, self).form_valid(form)

    def get_success_url(self):
        if qanda_messages:
            messages.success(self.request, self.message)
        question = self.get_object()
        return reverse('qanda_question_view',
                       kwargs={'pk': question.pk, 'slug': question.slug})

# NewCommentOnQuestionView

# EditCommentOnQuestionView

# NewAnswerView

# EditAnswerView

# NewCommentOnAnswerView

# EditCommentOnAnswerView

# DocumentView
class DocumentView(QandaBaseView, DetailView):
    model = Document
    template_name = 'qanda/detail.html'

    def html_content(self):
        return self.object.html_content

    def get(self, request, **kwargs):
        self.object = self.get_object()
        if self.request.path != self.object.get_absolute_url():
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

# CreateDocumentView
class CreateDocumentView(QandaBaseView, CreateView):
    """
    Create a document
    """
    template_name = 'qanda/create_form.html'
    message = _('Thank you! your document has been created.')
    form_class = DocumentForm

    def form_valid(self, form):
        """
        Create the required relation
        """
        form.instance.user = self.request.user
        return super(CreateDocumentView, self).form_valid(form)

    def get_success_url(self):
        if qanda_messages:
            messages.success(self.request, self.message)

        return reverse('qanda_index')

# UpdateDocumentView
class UpdateDocumentView(QandaBaseView, UpdateView):
    """
    Update a document
    """
    template_name = 'qanda/update_form.html'
    message = _('Thank you! your document has been updated.')
    form_class = DocumentForm
    model = Document
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        """
        Create the required relation
        """
        form.instance.user = self.request.user
        return super(UpdateDocumentView, self).form_valid(form)

    def get_success_url(self):
        if qanda_messages:
            messages.success(self.request, self.message)
        document = self.get_object()
        return reverse('qanda_document_view',
                       kwargs={'pk': document.pk, 'slug': document.slug})

# NewCommentOnDocumentView

# EditCommentOnDocumentView

# VoteView

# QuestionVoteView

# AnswerVoteView

# DocumentVoteVIew
