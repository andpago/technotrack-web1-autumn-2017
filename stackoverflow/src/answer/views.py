from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from .models import Answer


class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'question']
        widgets = {'question': forms.HiddenInput}


@method_decorator(login_required, name='dispatch')
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