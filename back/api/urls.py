from django.urls import path, include
from rest_framework import routers
from api import views
from .views import create_test

router = routers.DefaultRouter()
router.register(r"students", views.StudentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("test/", create_test, name="create_test"),
    # path('test/<int:test_id>/assign/', assign_test, name='assign_test'),
]
