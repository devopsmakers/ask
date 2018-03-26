from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='qanda_index'),
    url(r'^search/?$', views.SearchResultsView.as_view(), name='qanda_search'),
    url(r'^unanswered/$', views.UnansweredView.as_view(), name='qanda_unanswered'),
    url(r'^help/$', views.HelpView.as_view(), name='qanda_help'),

    url(r'^questions/ask/$', login_required(views.AskQuestionView.as_view()),
        name='qanda_ask_question'),

    url(r'^questions/(?P<pk>[\d]+)/(?P<slug>[\w-]+)/update$',
        login_required(views.UpdateQuestionView.as_view()),
        name='qanda_update_question_view'),

    url(r'^questions/(?P<pk>[\d]+)/(?P<slug>[\w-]+)/answer$',
        login_required(views.QuestionView.as_view()),
        name='qanda_question_answer_view'),

    url(r'^questions/(?P<pk>[\d]+)/(?P<slug>[\w-]+)/$',
        views.QuestionView.as_view(),
        name='qanda_question_view'),

    url(r'^documents/create/$', login_required(views.CreateDocumentView.as_view()),
        name='qanda_create_document'),

    url(r'^documents/(?P<pk>[\d]+)/(?P<slug>[\w-]+)/update$',
        login_required(views.UpdateDocumentView.as_view()),
        name='qanda_update_document_update'),

    url(r'^documents/(?P<pk>[\d]+)/(?P<slug>[\w-]+)/$',
        views.DocumentView.as_view(),
        name='qanda_document_view'),
]
