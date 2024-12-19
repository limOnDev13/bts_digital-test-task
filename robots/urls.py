from django.urls import path

from .views import create_robot, get_summary_in_file

app_name = "robots"

urlpatterns = [
    path("", create_robot, name="create_robots"),
    path("summary/", get_summary_in_file, name="summary"),
]
