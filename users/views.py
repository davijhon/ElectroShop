from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm



class SignupPageView(generic.CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('shop:profile')
	template_name = 'account/signup.html'
