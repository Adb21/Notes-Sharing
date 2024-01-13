from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from operations.models import Notes
from operations.serializers import NoteSerializer


# Create your views here.
class NotesListCreateAPIView(ModelViewSet):
    queryset = Notes.objects.none()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    # filter_backends = [DjangoFilterBackend, SearchFilter]

    def get_queryset(self):
        user = self.request.user
        queryset = Notes.objects.filter(created_by=user).order_by("created_at")
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().values("id", "title"))
        page = self.paginate_queryset(queryset)
        return self.get_paginated_response(page)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(data={"message": "Deleted record successfully"}, status=204)
