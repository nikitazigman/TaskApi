from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(prefix="tasks", viewset=views.TaskViewSet, basename="task")

urlpatterns = router.urls
