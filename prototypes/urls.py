from django.urls import path,include
from .views import IndexView,PrototypeDetailView,PrototypeCreateView,PrototypeDeleteView



app_name = 'Prototypes'
urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('prototypes/<int:pk>/',PrototypeDetailView.as_view(),name='detail'),
    path('prototypes/create/', PrototypeCreateView.as_view(), name='create'),
    path('prototypes/<int:pk>/delete/', PrototypeDeleteView.as_view(), name='delete'),
]
