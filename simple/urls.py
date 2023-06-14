from django.urls import path

from .controllers import SimpleAPI

urlpatterns = [
    path("", SimpleAPI.as_view(), name="simple"),
]
