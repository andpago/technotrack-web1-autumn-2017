# Create your views here.
from django.views.generic import DetailView
from .models import User


class UserDetailView(DetailView):
    model = User
    template_name = 'core/user.html'