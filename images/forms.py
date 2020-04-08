from django import forms
from . import models

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = models.Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput
        }