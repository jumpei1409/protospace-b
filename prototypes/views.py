from .models import Prototype
from django.views.generic import ListView, CreateView
from .forms import PrototypeForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(ListView):
    model = Prototype
    template_name = 'prototypes/index.html'
    context_object_name = 'prototypes'

class PrototypeCreateView(LoginRequiredMixin, CreateView):
    login_url = '/users/sign_in/'
    form_class = PrototypeForm
    template_name = 'prototypes/create.html'
    success_url = reverse_lazy('Prototypes:index')

    def form_valid(self, form):
        prototype = form.save(commit=False)
        prototype.user = self.request.user
        prototype.save()
        return super().form_valid(form)