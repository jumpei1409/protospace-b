from .models import Prototype
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .forms import PrototypeForm

class IndexView(ListView):
    model = Prototype
    template_name = 'prototypes/index.html'
    context_object_name = 'prototypes'

class PrototypeUpdateView(LoginRequiredMixin, UpdateView):
    model = Prototype
    form_class = PrototypeForm
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
