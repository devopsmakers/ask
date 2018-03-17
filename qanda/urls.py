from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.SearchView.as_view(), name='qanda_index'),
    url(r'^new-question/$', views.NewQuestionView.as_view(),
        name='qanda_new_question'),
    url(r'^new-document/$', views.NewDocumentView.as_view(),
        name='qanda_new_document'),
]
