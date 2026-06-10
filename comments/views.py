from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from .models import Comment
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from prototypes.models import Prototype

class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.prototype = get_object_or_404(Prototype, pk=self.kwargs['pk'])
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Prototypes:detail', kwargs={'pk': self.kwargs['pk']})