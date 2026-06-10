from .views import CommentCreateView
from django.urls import path

app_name = 'Comment'
urlpatterns = [
    path('<int:pk>/',CommentCreateView.as_view(),name='comment'),
]
