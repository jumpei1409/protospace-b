from .models import Prototype
from django.views.generic import ListView,DetailView
from comments.forms import CommentForm
from django.views.generic.edit import FormMixin
from comments.models import Comment 

class IndexView(ListView):
    model = Prototype
    template_name = 'prototypes/index.html'
    context_object_name = 'prototypes'

class DetailView(FormMixin,DetailView):
    model = Prototype
    form_class = CommentForm
    template_name = 'prototypes/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(prototype=self.object)
        context['comments'] = comments
        context['form'] = self.get_form()
        return context
