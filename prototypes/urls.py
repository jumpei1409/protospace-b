from django.urls import path,include
from .views import IndexView, PrototypeCreateView, PrototypeDetailView

app_name = 'Prototypes'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('prototypes/create/', PrototypeCreateView.as_view(), name='create'),
    path('prototypes/<int:pk>/detail',PrototypeDetailView.as_view(),name='detail'),
]