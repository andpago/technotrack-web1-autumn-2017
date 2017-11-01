from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.template import Library, Template
from django.template.loader import render_to_string
from django.urls import reverse

from question.models import Question

from question.models import Answer

register = Library()
User = get_user_model()


@register.simple_tag(takes_context=True)
def linkto(context, obj, **kwargs):
    cls = type(obj)
    if cls not in linkto.info_getters.keys():
        raise Exception("cannot create link to an object of type " + cls)

    info = linkto.info_getters[type(obj)](obj)
    info.update(kwargs)

    return render_to_string('core/tagtemplates/linkto.html', info)

linkto.info_getters = {
    User: lambda user: {
        'text': '@' + user.username,
        'url': reverse('core:user', kwargs={'slug': user.username})
    },
    Question: lambda question: {
        'text': question.title,
        'url': reverse('question:question', kwargs={'pk': question.id})
    },
    Answer: lambda answer: {
        'text': answer.text[:15] + '...',
        'url': reverse('question:question', kwargs={'pk': answer.question.id})
    },
}