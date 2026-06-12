from .models import Prototype
from django.views.generic import ListView,DetailView,CreateView,DeleteView,UpdateView
from comments.forms import CommentForm
from comments.models import Comment 
from django.views.generic.edit import FormMixin
from .forms import PrototypeForm,PrototypeUpdateForm
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

class IndexView(ListView):
    model = Prototype
    template_name = 'prototypes/index.html'
    context_object_name = 'prototypes'

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

class PrototypeDeleteView(LoginRequiredMixin, DeleteView):
    model = Prototype
    success_url = reverse_lazy('Prototypes:index')
    login_url = '/users/sign_in/'
    template_name = 'prototypes/detail.html'

    def get_queryset(self):
        return Prototype.objects.filter(user=self.request.user)
      
class PrototypeUpdateView(LoginRequiredMixin, UpdateView):
    model = Prototype
    form_class = PrototypeUpdateForm
    template_name = 'prototypes/update.html'

    def get(self, request, *args, **kwargs):
        prototype = self.get_object()
        # 自分の投稿でなければトップへ
        if prototype.user != request.user:
            return redirect(reverse('Prototypes:index'))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        prototype = self.get_object()
        # 自分の投稿でなければトップへ
        if prototype.user != request.user:
            return redirect(reverse('Prototypes:index'))
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        # 編集成功後は詳細ページへ
        return reverse('Prototypes:detail', kwargs={'pk': self.object.pk})
      
