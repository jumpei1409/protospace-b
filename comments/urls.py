from .views import CommentCreateView
from django.urls import path

app_name = 'Comment'
urlpatterns = [
    path('',CommentCreateView.as_view(),name='create'),
]
