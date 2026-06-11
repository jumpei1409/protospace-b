from django.urls import path
from .views import IndexView, CreateView, DeleteView

app_name = 'Prototypes'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create/', CreateView.as_view(), name='create'),
    path('<int:pk>/delete/', DeleteView.as_view(), name='delete'),
]