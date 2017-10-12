from django.conf.urls import url

from .views import QuestionDetailView, QuestionListView

urlpatterns = [
    url(r'^(?P<pk>\d+)$', QuestionDetailView.as_view(), name='question'),
    url(r'^every$', QuestionListView.as_view(), name='question_list'),
]