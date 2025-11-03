from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ("student", "Student"),
        ("professor", "Professor"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default="student")

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
