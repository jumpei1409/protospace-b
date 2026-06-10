from django.db import models
from django.conf import settings

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prototype = models.ForeignKey('prototypes.Prototype', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    