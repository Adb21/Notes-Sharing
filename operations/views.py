from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from operations.models import Notes
from operations.serializers import NoteSerializer


# Create your views here.
class NotesCRUDView(ModelViewSet):
    """Note CRUD operation View"""

    queryset = Notes.objects.none()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["title", "content"]

    def get_queryset(self):
        user = self.request.user
        uid = self.request.GET.get("uid")
        if uid:
            # Add Validations
            queryset = Notes.objects.filter(shareble_id=uid).first()
        else:
            queryset = Notes.objects.filter(created_by=user).order_by("created_at")
        return queryset

    def list(self, request, *args, **kwargs):
        uid = self.request.GET.get("uid")
        if uid:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset)
            data = serializer.data
            return Response(data=data)

        queryset = self.filter_queryset(self.get_queryset().values("id", "title"))
        page = self.paginate_queryset(queryset)
        return self.get_paginated_response(page)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            data={"message": "Deleted record successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class NoteSharingView(APIView):
    """Note Sharing View"""

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            note = Notes.objects.get(pk=id)
        except Notes.DoesNotExist:
            return Response(
                {"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND
            )

        sharable_id = Notes.generate_sharable_id(note)
        data = {"sharable_id": sharable_id}
        return Response(data=data, status=status.HTTP_200_OK)
