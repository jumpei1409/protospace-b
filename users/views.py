from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth import login, get_user_model
from .forms import CustomUserCreationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
# from tweets.models import Tweet

class SignInView(LoginView):
    template_name = 'users/sign_in.html'
    redirect_authenticated_user = True  # ログイン済みならリダイレクト
    
    def get_success_url(self):
        return reverse_lazy('Prototypes:index')

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('Prototypes:index')  # 登録完了後にリダイレクトするURL
    template_name = 'users/sign_up.html'

    def form_valid(self, form):
        # バリデーションが成功したら、ユーザーを作成してそのユーザーでログインさせる
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response