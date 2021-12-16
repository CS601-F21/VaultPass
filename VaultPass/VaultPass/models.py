from django.db import models
from django.contrib.auth.models import User

class Password(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    siteTitle = models.CharField(max_length=50)
    pwd = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    hint = models.CharField(max_length=50, default="", null=True)
    siteLogo = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.siteTitle

    class Meta:
        ordering = ["-id"]    