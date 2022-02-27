from django.db import models
from django.utils import timezone


class Day(models.Model):
    user_id = models.IntegerField()
    date_created = models.DateField(auto_now=False)

    def __str__(self):
        return f"List: {self.date_created.strftime('%Y/%m/%d')}"

    class Meta:
        ordering = ["-date_created"]
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "date_created"], name="unique_user_date_created"
            ),
        ]


class Task(models.Model):
    user_id = models.IntegerField()

    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    difficulty = models.IntegerField(default=1)
    deadline = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    day = models.ForeignKey(
        Day, related_name="tasks", null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["deadline"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(difficulty__gte=1) & models.Q(difficulty__lte=11),
                name="check_difficulty_range",
            ),
        ]
