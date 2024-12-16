from django.urls import path

from .views import create_robot

app_name = "robots"

urlpatterns = [path("", create_robot, name="create_robots")]
