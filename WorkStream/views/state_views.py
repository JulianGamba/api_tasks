from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from WorkStream.models import State
from WorkStream.serializers import (
    StateSerializer
)

from WorkStream.permissions import IsAuthenticatedOrReadOnly, IsOwnerOrAssignedUser, IsCommentOwner

@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Obtiene una lista de todos los estados.",
        responses={200: StateSerializer(many=True)},
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Obtiene un estado específico por ID.",
        responses={200: StateSerializer, 404: "Not Found"},
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Crea un nuevo estado. Acepta múltiples estados si se envía una lista.",
        request_body=StateSerializer(many=True),
        responses={201: StateSerializer(many=True)},
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Actualiza un estado específico por ID.",
        request_body=StateSerializer,
        responses={200: StateSerializer, 400: "Bad Request", 404: "Not Found"},
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Actualiza parcialmente un estado específico por ID.",
        request_body=StateSerializer,
        responses={200: StateSerializer, 400: "Bad Request", 404: "Not Found"},
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Elimina un estado específico por ID.",
        responses={204: "No Content", 404: "Not Found"},
    ),
)
class StateViewSet(viewsets.ModelViewSet):

    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        # Si los datos enviados son una lista, muchos=True se aplica automáticamente
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list)
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()