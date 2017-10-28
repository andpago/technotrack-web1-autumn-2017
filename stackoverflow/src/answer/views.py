from django import forms
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView

from .models import Answer
from question.models import Question


class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'question']
        widgets = {'question': forms.HiddenInput}


class CreateAnswerView(CreateView):
    form_class = AnswerCreateForm

    def get(self, request, *args, **kwargs):
        raise Http404

    def form_valid(self, form):
        answer = form.save(commit=False)
        answer.author = self.request.user
        answer.save()

        return super(CreateAnswerView, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponseBadRequest("<h1>Bad request</h1>")