from django.conf.urls import url

from .views import QuestionDetailView

urlpatterns = [
    url(r'^(?P<pk>\d+)$', QuestionDetailView.as_view(), name='question')
]