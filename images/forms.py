from django import forms
from . import models
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = models.Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput
        }
        """
            Users will not enter the image URL directly in the form. Instead, we will provide them with a JavaScript tool to choose an image from an external site, and our form will receive its URL as a parameter. We override the default widget of the url field to use a HiddenInput widget. This widget is rendered as an HTML input element with a type="hidden" attribute. We use this widget because we don't want this field to be visible to users.
        """

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions')
        return url

    def save(self, force_insert=False,
                force_update=False,
                commit=True):
        image = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title),
                                image_url.rsplit('.', 1)[1].lower())

        # download image from the given URL
        response = request.urlopen(image_url)
        image.image.save(image_name,
                        ContentFile(response.read()),
                        save=False)
        if commit:
            image.save()
        return image