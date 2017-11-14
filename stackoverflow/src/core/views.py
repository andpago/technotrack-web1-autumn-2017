# Create your views here.
from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, FormView
from django.contrib.auth.password_validation import validate_password

from question.models import Question, Answer
from category.models import QuestionCategory
from .models import User


def has_search_form(sort_choices):
    class SearchForm(forms.Form):
        search = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
        sort = forms.ChoiceField(choices=sort_choices, required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    def decorator(Class: type):
        class NewClass(Class):
            def get_queryset(self):
                q = super(self.__class__, self).get_queryset()
                self.search_form = SearchForm(self.request.GET)

                if self.search_form.is_valid():
                    if self.search_form.cleaned_data['search']:
                        q = q.filter(text__contains=self.search_form.cleaned_data['search'])

                    if self.search_form.cleaned_data['sort']:
                        q = q.order_by(self.search_form.cleaned_data['sort'])

                return q

            def get_context_data(self, **kwargs):
                context = super(self.__class__, self).get_context_data(**kwargs)
                context['search_form'] = self.search_form

                return context
        NewClass.__name__ = Class.__name__

        return NewClass

    return decorator


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

        context['questions'] = Question.objects.order_by('-created')[:5]
        context['answers'] = Answer.objects.order_by('-created')[:5]

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

        return super(RegisterView, self).form_valid(form)