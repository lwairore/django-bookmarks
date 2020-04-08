from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.
class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug= models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True) # We use `bd_index=True` so that Django creates an index in the database for this field.
    """
        Database indexes improve query performance. Consider setting db_index=True for fields that you frequently query using filter(), exclude(), or order_by(). ForeignKey fields or fields with unique=True imply the creation of an index. You can also use Meta.index_together to create indexes for multiple fields.
    """
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
            we use the slugify() function provided by Django to automatically generate the image slug for the given title when no slug is provided. Then, we save the object. We will generate slugs for images automatically so that users don't have to manually enter a slug for each image.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)
        

