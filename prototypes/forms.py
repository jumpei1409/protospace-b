from django import forms
from .models import Prototype


class PrototypeForm(forms.ModelForm):
    class Meta:
        model = Prototype
        fields = ['title', 'catchphrase', 'concept', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 編集時は画像を必須にしない（未変更でも保存できるように）
        self.fields['image'].required = False