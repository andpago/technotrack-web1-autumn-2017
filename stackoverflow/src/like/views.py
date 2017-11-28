from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseBadRequest, HttpResponse, HttpResponseForbidden
# Create your views here.
from django.views.decorators.csrf import csrf_protect
from question.models import Answer, Question

from .models import Like


@csrf_protect
def create_like(request, *args, **kwargs):
    if request.method != "POST":
        raise Http404
    else:
        if request.user.is_anonymous():
            return HttpResponseForbidden()

        allowed_models = {
            'question': Question,
            'answer': Answer
        }

        if all(name in request.POST for name in ('model_name', 'object_id')):
            model_name = request.POST['model_name']
            object_id = request.POST['object_id']
            user = request.user

            if model_name not in allowed_models:
                return HttpResponseBadRequest()

            try:
                like = Like.objects.get(content_type=ContentType.objects.get(model=model_name), user=user)
                like.delete()

                return HttpResponse('off')
            except Like.DoesNotExist:
                model = allowed_models[model_name]

                try:
                    obj = model.objects.get(id=object_id)
                except ObjectDoesNotExist:
                    return HttpResponseBadRequest()

                like = Like(object=obj, user=request.user)

                like.save()

                return HttpResponse('on')

        else:
            return HttpResponseBadRequest()


def delete_like():
    pass