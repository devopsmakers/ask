from django.shortcuts import render
from django.views.generic import FormView, View, CreateView
from django.conf import settings
from django.utils.translation import ugettext as _
from django.urls import reverse
from .forms import SearchForm, QuestionForm, DocumentForm
from .models import Question, Document

try:
    qa_messages = 'django.contrib.messages' in settings.INSTALLED_APPS and \
        settings.QANDA_SETTINGS['messages']

except AttributeError:  # pragma: no cover
    qa_messages = False

if qa_messages:
    from django.contrib import messages

# Create your views here.


# QandaBaseView
class QandaBaseView(View):
    def get_context_data(self, **kwargs):
        context = super(QandaBaseView, self).get_context_data(**kwargs)
        context['ORGANIZATION_NAME'] = settings.QANDA_SETTINGS.get(
            'organization', '')
        context['LOGO'] = settings.QANDA_SETTINGS.get(
            'logo', False)
        context['unanswered_count'] = Question.objects.unanswered().count()
        return context


# SearchView
class SearchView(QandaBaseView, FormView):
    """ Main index / search view """
    template_name = 'qanda/index.html'
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['nav'] = 'search'
        return context


# SearchResultsView

# QuestionDetailView


# NewQuestionView
class NewQuestionView(QandaBaseView, CreateView):
    """
    Create a question
    """
    template_name = 'qanda/create_form.html'
    message = _('Thank you! your question has been created.')
    form_class = QuestionForm

    def form_valid(self, form):
        """
        Create the required relation
        """
        form.instance.user = self.request.user
        return super(NewQuestionView, self).form_valid(form)

    def get_success_url(self):
        if qa_messages:
            messages.success(self.request, self.message)

        return reverse('qanda_index')


# EditQuestionView

# NewCommentOnQuestionView

# EditCommentOnQuestionView

# NewAnswerView

# EditAnswerView

# NewCommentOnAnswerView

# EditCommentOnAnswerView

# NewDocumentView
class NewDocumentView(QandaBaseView, CreateView):
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
        return super(NewDocumentView, self).form_valid(form)

    def get_success_url(self):
        if qa_messages:
            messages.success(self.request, self.message)

        return reverse('qanda_index')

# EditDocumentView

# NewCommentOnDocumentView

# EditCommentOnDocumentView

# VoteView

# QuestionVoteView

# AnswerVoteView

# DocumentVoteVIew
