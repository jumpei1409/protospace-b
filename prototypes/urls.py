from django.urls import path,include
from .views import IndexView, PrototypeUpdateView



app_name = 'Prototypes'
urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('prototypes/<int:pk>/update', PrototypeUpdateView.as_view(), name='update'),
]
