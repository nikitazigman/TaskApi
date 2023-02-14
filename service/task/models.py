from django.db import models
from django.contrib.auth import get_user_model
from day.models import Day


class Task(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)

    title = models.CharField(max_length=150)
    level = models.IntegerField(default=1)
    deadline = models.DateField(auto_now=False, blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    day = models.ForeignKey(to=Day, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return (
            f"Task(title={self.title}, level={self.level},"
            f" deadline={self.deadline}, compleated_at={self.completed_at},"
            f" day={self.day})"
        )

    class Meta:
        ordering = ["deadline"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(level__gte=1) & models.Q(level__lte=10),
                name="check_difficulty_range",
            ),
        ]
