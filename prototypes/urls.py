from django.urls import path,include
from .views import IndexView



app_name = 'Prototypes'
urlpatterns = [
    path('prototypes/index',IndexView.as_view(),name='index'),
]
