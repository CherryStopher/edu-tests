from django.urls import path, include
from rest_framework import routers
from api import views
from .views import create_test

router = routers.DefaultRouter()
router.register(r"students", views.StudentViewSet)

urlpatterns = [ 
    path('test/', create_test, name='create_test')
    ]
