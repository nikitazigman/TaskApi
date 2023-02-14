from django.db import models
from django.contrib.auth import get_user_model


class Day(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    date = models.DateField(unique=True, auto_now=False, auto_created=False)

    class Meta:
        ordering = ["date"]

    def __str__(self) -> str:
        return str(self.date)
