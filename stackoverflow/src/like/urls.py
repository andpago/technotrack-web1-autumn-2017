from django.conf.urls import url
from .views import like_question, like_answer

urlpatterns = [
    url(r'^question$', like_question, name='like_question'),
    url(r'^answer$', like_answer, name='like_answer'),
]
