from django.conf.urls import url

from .views import QuestionDetailView, QuestionListView, QuestionCreateView
from answer.views import CreateAnswerView

urlpatterns = [
    url(r'^(?P<pk>\d+)/create_answer$', CreateAnswerView.as_view(), name='create_answer'),
    url(r'^(?P<pk>\d+)$', QuestionDetailView.as_view(), name='question'),
    url(r'^every$', QuestionListView.as_view(), name='question_list'),
    url(r'^create$', QuestionCreateView.as_view(), name='create'),
]
