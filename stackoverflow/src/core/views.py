# Create your views here.
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, FormView
from django.contrib.auth.password_validation import validate_password

from answer.models import Answer
from question.models import Question
from category.models import QuestionCategory
from .models import User


class UserDetailView(DetailView):
    model = User
    template_name = 'core/user.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = self.get_object()

        context['user_questions'] = user.questions.all()[:5]
        context['user_answers'] = user.answers.all()[:5]

        return context


class HomeView(View):
    def get(self, request, **kwargs):
        if 'context' in kwargs:
            context = kwargs['context']
        else:
            context = {}

        context['questions'] = Question.objects.all()[:5]
        context['answers'] = Answer.objects.all()[:5]

        context['cat_count'] = QuestionCategory.objects.count()
        context['qsn_count'] = Question.objects.count()
        context['ans_count'] = Answer.objects.count()
        context['usr_count'] = User.objects.count()

        kwargs['context'] = context

        return render(request, 'core/home.html', **kwargs)


class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)


class RegisterView(FormView):
    template_name = 'core/register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        user = User()

        if User.objects.filter(username=form.cleaned_data['username']):
            return redirect(to='/register?bad=username')

        user.username = form.cleaned_data['username']
        try:
            validate_password(form.cleaned_data['password'])
        except ValidationError:
            return redirect(to='/register?bad=password')
        user.set_password(form.cleaned_data['password'])
        user.save()

        print(user)

        return super(RegisterView, self).form_valid(form)