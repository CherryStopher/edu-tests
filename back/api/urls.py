from django.urls import path, include
from rest_framework import routers
from api import views
from .views import (
    assign_test,
    create_test,
    get_test_by_id,
    get_tests,
    manage_test_scores,
)

router = routers.DefaultRouter()
router.register(r"students", views.StudentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("tests/", get_tests, name="get_tests"),
    path("test/", create_test, name="create_test"),
    path("test/<int:test_id>", get_test_by_id, name="get_test_by_id"),
    path("test/<int:test_id>/assign/", assign_test, name="assign_test"),
    path("test/<int:test_id>/answers/", manage_test_scores, name="manage_test_scores"),
]
