from django.urls import path,include
from .views import IndexView, CreateView, DetailView

app_name = 'Prototypes'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('prototypes/create/', CreateView.as_view(), name='create'),
    path('prototypes/<int:pk>/detail',DetailView.as_view(),name='detail'),
]