from django.conf.urls import url

from .views import QuestionDetailView, QuestionListView, QuestionCreateView, QuestionEditView, AnswerEditView, \
    CreateAnswerView, ajax_get_question, ajax_get_answer

urlpatterns = [
    url(r'^(?P<pk>\d+)/create_answer$', CreateAnswerView.as_view(), name='create_answer'),
    url(r'^(?P<pk>\d+)/edit$', QuestionEditView.as_view(), name='edit_question'),
    url(r'^(?P<pk>\d+)$', QuestionDetailView.as_view(), name='question'),
    url(r'^every$', QuestionListView.as_view(), name='question_list'),
    url(r'^create$', QuestionCreateView.as_view(), name='create'),
    url(r'^ajax/get/question/(\d+)$', ajax_get_question),
    url(r'^ajax/get/answer/(\d+)$', ajax_get_answer),
]


urlpatterns += [
    url(r'^edit_answer/(?P<pk>\d+)$', AnswerEditView.as_view(), name='edit_answer'),
]