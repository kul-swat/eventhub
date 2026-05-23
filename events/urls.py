from rest_framework.routers import DefaultRouter
from .views import EventViewSet, ReservationViewSet

# Use DefaultRouter and router.register() exactly as shown in class:

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'reservations', ReservationViewSet, basename='reservation')

urlpatterns = router.urls
