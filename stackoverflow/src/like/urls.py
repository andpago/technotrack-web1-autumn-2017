from django.conf.urls import url

from .views import create_like

urlpatterns = [
    url(r'^create$', create_like, name='create')
]