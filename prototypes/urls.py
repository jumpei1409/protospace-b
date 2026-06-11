from django.urls import path
from .views import IndexView, PrototypeCreateView

app_name = 'Prototypes'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create/', PrototypeCreateView.as_view(), name='create'),
]