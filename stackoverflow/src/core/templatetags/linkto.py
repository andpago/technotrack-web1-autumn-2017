from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.template import Library, Template

register = Library()
User = get_user_model()


@register.simple_tag(takes_context=True)
def linkto(context, obj):
    context.update({'object': obj})

    cls = obj.__class__.__name__

    if cls not in linkto.links.keys():
        raise Exception("cannot create link to an object of type " + cls)

    return Template('<a href={% url \'' + linkto.links[cls] + '\' object.' + linkto.args[cls] + ' %}>' + linkto.text[cls] + '</a>').render(context)

linkto.links = {
    'User': 'core:user',
    'Question': 'question:question',
    'Answer': 'question:question'
}

linkto.args = {
    'User': 'username',
    'Question': 'pk',
    'Answer': 'question.pk'
}

linkto.text = {
    'User': '@{{ object.username }}',
    'Question': '{{object.title}}',
    'Answer': '{{object.text|truncatechars:20}}'
}