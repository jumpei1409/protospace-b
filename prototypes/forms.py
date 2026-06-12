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
    
class PrototypeUpdateForm(PrototypeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False  # 編集時のみ任意
