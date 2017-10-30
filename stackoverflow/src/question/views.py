from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, CreateView, FormView, UpdateView

from answer.views import AnswerCreateForm
from martor.fields import MartorFormField

from .models import Question


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'question/question.html'

    def get_context_data(self, **kwargs):
        answer_form = AnswerCreateForm(initial={'question': self.get_object()})

        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['answer_form'] = answer_form

        return context


class SearchForm(forms.Form):
    search = forms.CharField(required=False)


def has_search_form(Class):
    class NewClass(Class):
        def get_queryset(self):
            print(self.__class__)
            q = super(self.__class__, self).get_queryset()
            self.search_form = SearchForm(self.request.GET)

            if self.search_form.is_valid():
                if self.search_form.cleaned_data['search']:
                    q = q.filter(text__contains=self.search_form.cleaned_data['search'])

            return q

        def get_context_data(self, **kwargs):
            context = super(self.__class__, self).get_context_data(**kwargs)
            context['search_form'] = self.search_form

            return context
    NewClass.__name__ = Class.__name__

    return NewClass


@has_search_form
class QuestionListView(ListView):
    model = Question
    template_name = 'question/question_list.html'


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'category']


@method_decorator(login_required, name='dispatch')
class QuestionCreateView(CreateView):
    template_name = 'question/question_create.html'
    form_class = QuestionCreateForm

    def form_valid(self, form):
        question = form.save(commit=False)
        question.author = self.request.user
        question.save()

        return super(QuestionCreateView, self).form_valid(form)


def author_only(f):
    def res(self, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return HttpResponseForbidden("<h1>You cannot edit this entry</h1>")
        else:
            return f(self, *args, **kwargs)
    return res


def author_only_methods(*args):
    def decorator(Class):
        for arg in args:
            setattr(Class, arg, author_only(getattr(Class, arg)))

        return Class
    return decorator


@author_only_methods('get', 'post')
@method_decorator(login_required, name='dispatch')
class QuestionEditView(UpdateView):
    template_name = 'question/question_edit.html'
    model = Question
    fields = ['title', 'text', 'category']