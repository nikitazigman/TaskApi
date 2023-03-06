from day.models import Day
from django.contrib.auth import get_user_model
from django.db import models


class Task(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)

    title = models.CharField(max_length=150)
    level = models.IntegerField(default=1)
    deadline = models.DateField(auto_now=False, blank=True, null=True)
    completed_at = models.ForeignKey(
        to=Day,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="completed_tasks",
        default=None,
    )

    @property
    def completed(self) -> bool:
        return bool(self.completed_at)

    @completed.setter
    def completed(self, status: bool) -> None:
        """Assigns the latest assigned day to the completed_at property if status is True

        The client can complete task only in a Today page,
        so the method on True status assigns the latest day from days property

        Args:
            status (bool): True - completed, False - active

        Raises:
            TypeError: setter accept only bool values
        """

        if type(status) != bool:
            raise TypeError("The property accept only bool type")

        if not status:
            self.completed_at = None
            return None

        if len(self.days.all()) == 0:
            raise RuntimeError(
                "The task cannot be completed since the task object does not have any assigned days"
            )

        self.completed_at = self.days.order_by("-date").first()

    days = models.ManyToManyField(to=Day, blank=True, related_name="assigned_tasks")

    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"Task={self.title}, level={self.level}"

    class Meta:
        ordering = ["deadline"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(level__gte=1) & models.Q(level__lte=10),
                name="check_difficulty_range",
            ),
        ]
