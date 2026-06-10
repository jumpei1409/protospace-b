from django.db import models
from django.conf import settings

class Prototype(models.Model):
  class Meta:
    db_table = 'prototypes'

  title = models.CharField(max_length=100, null=False, blank=False)
  catchphrase = models.CharField(max_length=200, null=False, blank=False)
  concept = models.TextField(null=False, blank=False)
  image = models.ImageField(upload_to='images/', blank=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)