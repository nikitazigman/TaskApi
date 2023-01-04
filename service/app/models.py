from django.contrib.auth.models import User as DefaultUser
from django.db import models


class Task(models.Model):
    user = models.ForeignKey(DefaultUser, on_delete=models.CASCADE)

    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    level = models.IntegerField(default=1)
    deadline = models.DateField(auto_now=False, blank=False, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    date = models.DateField(auto_now=False, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["deadline"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(level__gte=1) & models.Q(level__lte=11),
                name="check_difficulty_range",
            ),
        ]
