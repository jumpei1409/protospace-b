from django.urls import path,include
from .views import IndexView,PrototypeDetailView



app_name = 'Prototypes'
urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('prototypes/<int:pk>/detail',PrototypeDetailView.as_view(),name='detail'),
]
