"""stack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.shortcuts import render

from src.core.views import rootView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', rootView),
    url(r'^user/(?P<username>\w+)$', lambda request, **kwargs: render(request, "core/user.html", kwargs)),
    url(r'^question/(?P<question_id>\d+)$', lambda request, **kwargs: render(request, "core/question.html", kwargs)),
]
