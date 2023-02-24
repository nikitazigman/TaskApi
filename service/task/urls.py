from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(prefix="tasks", viewset=views.TaskViewSet, basename="task")

urlpatterns = router.urls
