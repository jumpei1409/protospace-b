from django import forms
from .models import Prototype

class PrototypeForm(forms.ModelForm):
  class Meta:
    model = Prototype
    fields = ("title", "catchphrase", "concept", "image")
    labels = {
      'title': 'プロトタイプの名称',
      'catchphrase': 'キャッチコピー',
      'concept': 'コンセプト',
      'image': 'プロトタイプの画像',
    }