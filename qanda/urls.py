from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.SearchView.as_view(), name='qanda_index'),
]
