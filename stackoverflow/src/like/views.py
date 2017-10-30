from answer.models import Answer
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from question.models import Question


def get_like_view(Class):
    name = Class.__name__.lower()

    @login_required
    def like_function(request, *args, **kwargs):
        if request.method != "POST":
            return HttpResponseBadRequest('<h1>Method ' + request.method + ' is unsupported</h1>')
        else:
            user = request.user
            id = request.POST.get(name + '_id', None)
            LikeClass = globals()[Class.__name__ + 'Like']

            if id is None:
                return HttpResponseBadRequest('<h1>Bad request: no object specified</h1>')

            try:
                obj = Class.objects.get(id=id)
            except Class.DoesNotExist:
                return HttpResponseBadRequest('<h1>Bad request: object does not exist</h1>')

            try:
                old_like = LikeClass.objects.get(author=user, **{name + '_id': id})
                old_like.delete()
                return redirect(obj.get_absolute_url())
            except LikeClass.DoesNotExist:
                like = LikeClass(author=user, **{name + '_id': id})
                like.save()
                return redirect(obj.get_absolute_url())
            except LikeClass.MultipleObjectsReturned:
                # this is very bad :(
                for like in LikeClass.objects.filter(author=user, **{name + '_id': id}).all():
                    like.delete()

                return redirect('/')
    return like_function

like_answer = get_like_view(Answer)
like_question = get_like_view(Question)