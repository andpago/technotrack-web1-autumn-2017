from django.conf.urls import url
from .views import like_question

urlpatterns = [
    url(r'^question$', like_question, name='like_question'),
]
