from django.urls import include, path
from rest_framework.routers import DefaultRouter

from operations.views import NotesCRUDView, NoteSharingView

router = DefaultRouter()

router.register(r"", NotesCRUDView, basename="note")

urlpatterns = [
    path("", include(router.urls)),
    path("<int:id>/share", NoteSharingView.as_view(), name="note-share"),
]
