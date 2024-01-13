from django.urls import include, path
from rest_framework.routers import DefaultRouter

from operations.views import NoteSharingAPIView, NotesListCreateAPIView

router = DefaultRouter()

router.register(r"", NotesListCreateAPIView, basename="notes-list-create")

urlpatterns = [
    path("", include(router.urls)),
    path("<int:id>/share", NoteSharingAPIView.as_view(), name="note-share"),
]
