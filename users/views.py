from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth import login, get_user_model
from .forms import CustomUserCreationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView

User = get_user_model()

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
        login(self.request, self.object)     # self.objectを使う
        return response

class UserPageView(DetailView):
    model = User
    template_name = 'users/mypage.html'
    context_object_name = 'profile_user'  # 'user' 以外の名前にする

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ユーザー情報を同時に取得し、N+1問題を回避する
        context['prototypes'] = self.object.prototype_set.select_related('user').all()
        return context
