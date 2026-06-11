from django.urls import path
from .views import PrototypeIndexView, PrototypeCreateView, PrototypeDeleteView

app_name = 'Prototypes'
urlpatterns = [
    path('', PrototypeIndexView.as_view(), name='index'),
    path('create/', PrototypeCreateView.as_view(), name='create'),
    path('<int:pk>/delete/', PrototypeDeleteView.as_view(), name='delete'),
]