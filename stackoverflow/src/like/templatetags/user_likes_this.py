from django.contrib.contenttypes.models import ContentType
from django.template import Library

from like.models import Like

register = Library()


@register.simple_tag
def user_likes_this(type, user, object, **kwargs):

    try:
        Like.objects.get(content_type=ContentType.objects.get(model=type),
                         user=user,
                         object_id=object.id)
        return True
    except Like.DoesNotExist:
        return False
