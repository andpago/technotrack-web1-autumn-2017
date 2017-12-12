from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseBadRequest, Http404, HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, CreateView, FormView, UpdateView


from martor.fields import MartorFormField
from core.views import has_search_form, author_only_methods
from .models import Question, Answer


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'question/question.html'

    def get_context_data(self, **kwargs):
        answer_form = AnswerCreateForm(initial={'question': self.get_object()})

        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['answer_form'] = answer_form

        return context


@has_search_form(sort_choices=[
            ('title', 'title asc'),
            ('-title', 'title desc'),
            ('text', 'text asc'),
            ('-text', 'text desc'),
            ('author', 'author'),
            ('-author', 'author desc'),
            ('category', 'category asc'),
            ('-category', 'category desc')
])
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


@author_only_methods('get', 'post')
@method_decorator(login_required, name='dispatch')
class QuestionEditView(UpdateView):
    template_name = 'question/question_edit.html'
    model = Question
    fields = ['title', 'text', 'category']


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


@author_only_methods('get', 'post')
@method_decorator(login_required, name='dispatch')
class AnswerEditView(UpdateView):
    template_name = 'question/answer_edit.html'
    model = Answer
    fields = ['text']


def ajax_get_question(request, id):
    try:
        q = Question.objects.get(id=id)
        return render(request, 'question/block/question.html', {'question': q})
    except Question.DoesNotExist:
        return HttpResponse('')


def ajax_get_answer_ids_for_question(request, question_id):
    answers = Answer.objects.filter(question_id=question_id)

    return JsonResponse({"ids": [answer.id for answer in answers]})


def ajax_get_answers_top(request, n=5):
    try:
        n = int(n)
    except:
        n = 5
    if n > 20: n = 20
    answers = Answer.objects.all()[:n]

    return JsonResponse({'ids': [answer.id for answer in answers]})


def ajax_get_answer(request, id):
    try:
        a = Answer.objects.get(id=id)
        return render(request, 'question/block/answer.html', {'answer': a})
    except Answer.DoesNotExist:
        return HttpResponse('')


def ajax_get_answer_n_likes(request, id):
    try:
        a = Answer.objects.get(id=id)
        return JsonResponse({'n': a.count_likes()})
    except Answer.DoesNotExist:
        return JsonResponse({'n': 0})


def ajax_get_question_n_likes(request, id):
    try:
        q = Question.objects.get(id=id)
        return JsonResponse({'n': q.count_likes()})
    except Question.DoesNotExist:
        return JsonResponse({'n': 0})