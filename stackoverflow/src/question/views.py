from django import forms
from django.http import HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, FormView, UpdateView

from answer.views import AnswerCreateForm
from .models import Question


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'question/question.html'

    def get_context_data(self, **kwargs):
        answer_form = AnswerCreateForm(initial={'question': self.get_object()})

        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['answer_form'] = answer_form

        return context


class QuestionListView(ListView):
    model = Question
    template_name = 'question/question_list.html'


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']


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


class QuestionEditView(UpdateView):
    template_name = 'question/question_edit.html'
    model = Question
    fields = ['title', 'text']

    @author_only
    def get(self, *args, **kwargs):
        return super(QuestionEditView, self).get(*args, **kwargs)

    @author_only
    def post(self, *args, **kwargs):
        return super(QuestionEditView, self).post(*args, **kwargs)