from django.contrib.auth import get_user_model
from django.db import models


class Day(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_created=False)

    class Meta:
        ordering = ["date"]
        unique_together = ["user", "date"]

    def __str__(self) -> str:
        return f"{self.id} {self.date}"
