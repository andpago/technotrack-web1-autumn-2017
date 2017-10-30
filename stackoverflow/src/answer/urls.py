from django.conf.urls import url

from .views import AnswerEditView

urlpatterns = [
    url(r'^edit/(?P<pk>\d+)$', AnswerEditView.as_view(), name='edit_answer'),
]