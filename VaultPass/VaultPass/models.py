from django.db import models
from django.contrib.auth.models import User

class Password(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    siteTitle = models.CharField(max_length=100)
    pwd = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    siteLogo = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    class Metadata:
        ordering = ["-id"]    