from .models import Prototype
from django.views.generic import ListView

class IndexView(ListView):
    model = Prototype
    template_name = 'prototypes/index.html'
    context_object_name = 'prototypes'
