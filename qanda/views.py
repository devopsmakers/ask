from django.shortcuts import render
from django.views.generic import FormView
from django.conf import settings

from .forms import SearchForm

try:
    qa_messages = 'django.contrib.messages' in settings.INSTALLED_APPS and \
        settings.QANDA_SETTINGS['messages']

except AttributeError:  # pragma: no cover
    qa_messages = False

if qa_messages:
    from django.contrib import messages

# Create your views here.

# SearchView
class SearchView(FormView):
    """ Main index / search view """
    template_name = 'qanda/index.html'
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['nav'] = 'search'
        context['ORGANIZATION_NAME'] = settings.QANDA_SETTINGS.get(
            'organization', '')
        context['LOGO'] =  settings.QANDA_SETTINGS.get(
            'logo', False)
        return context


# SearchResultsView

# QuestionDetailView

# NewQuestionView

# EditQuestionView

# NewCommentOnQuestionView

# EditCommentOnQuestionView

# NewAnswerView

# EditAnswerView

# NewCommentOnAnswerView

# EditCommentOnAnswerView

# NewDocumentView

# EditDocumentView

# NewCommentOnDocumentView

# EditCommentOnDocumentView

# VoteView

# QuestionVoteView

# AnswerVoteView

# DocumentVoteVIew
