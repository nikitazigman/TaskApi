from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("days", viewset=views.DayViewSet, basename="day")

urlpatterns = router.urls
