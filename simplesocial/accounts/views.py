from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import UserCreateForm

# Create your views here.
class SignUp(CreateView):
    form_class = UserCreateForm

    # after successful registration it will take us to login page,
    # we're using reverse_lazy since if a user is not created properly then he won't be directed to the login page
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
