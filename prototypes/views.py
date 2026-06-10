from .models import Prototype
from django.views.generic import ListView, CreateView, DetailView
from .forms import PrototypeForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from comments.models import Comment 
from comments.forms import CommentForm

class IndexView(ListView):
    model = Prototype
    template_name = 'prototypes/index.html'
    context_object_name = 'prototypes'

class CreateView(LoginRequiredMixin, CreateView):
    login_url = '/users/sign_in/'
    form_class = PrototypeForm
    template_name = 'prototypes/create.html'
    success_url = reverse_lazy('Prototypes:index')

    def form_valid(self, form):
        prototype = form.save(commit=False)
        prototype.user = self.request.user
        prototype.save()
        return super().form_valid(form)
    
class PrototypeDetailView(FormMixin,DetailView):
    model = Prototype
    form_class = CommentForm
    template_name = 'prototypes/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(prototype=self.object)
        context['comments'] = comments
        context['form'] = self.get_form()
        return context