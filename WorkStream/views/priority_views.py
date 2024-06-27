from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from WorkStream.models import Priority
from WorkStream.permissions import IsAuthenticatedOrReadOnly
from WorkStream.serializers import PrioritySerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Obtiene una lista de todas las prioridades.",
        responses={200: PrioritySerializer(many=True)},
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Obtiene una prioridad específica por ID.",
        responses={200: PrioritySerializer, 404: "Not Found"},
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Crea una nueva prioridad. Acepta múltiples prioridades si se envía una lista.",
        request_body=PrioritySerializer(many=True),
        responses={201: PrioritySerializer(many=True)},
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Actualiza una prioridad específica por ID.",
        request_body=PrioritySerializer,
        responses={200: PrioritySerializer, 400: "Bad Request", 404: "Not Found"},
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Actualiza parcialmente una prioridad específica por ID.",
        request_body=PrioritySerializer,
        responses={200: PrioritySerializer, 400: "Bad Request", 404: "Not Found"},
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Elimina una prioridad específica por ID.",
        responses={204: "No Content", 404: "Not Found"},
    ),
)
class PriorityViewSet(viewsets.ModelViewSet):

    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
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
