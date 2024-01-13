from django.urls import include, path
from rest_framework.routers import DefaultRouter

from operations.views import NotesListCreateAPIView

router = DefaultRouter()

router.register(r"", NotesListCreateAPIView, basename="notes-list-create")

urlpatterns = [
    path("/", include(router.urls)),
]
