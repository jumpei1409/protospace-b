from django.shortcuts import render
from django.views.generic import ListView

class IndexView(ListView):
    class Meta:
        model = 'prototypes'
        template_list = 'index.html'
