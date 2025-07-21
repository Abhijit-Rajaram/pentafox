from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    role = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    class meta:
        ordering = ['role']
        indexes = [models.Index(fields=['role'])]

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name='user')
    role = models.ForeignKey(Role, on_delete=models.RESTRICT, related_name='role_assign')
    # status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    class meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user'])]
    