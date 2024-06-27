from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from WorkStream.models import CustomUser
from WorkStream.permissions import IsAuthenticatedOrReadOnly
from WorkStream.serializers import CustomUserSerializer, LoginSerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Obtiene una lista de todos los usuarios.",
        responses={200: CustomUserSerializer(many=True)},
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Obtiene un usuario específico por ID.",
        responses={200: CustomUserSerializer, 404: "Not Found"},
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Crea un nuevo usuario",
        request_body=CustomUserSerializer(many=True),
        responses={201: CustomUserSerializer(many=True)},
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Actualiza un usuario específico por ID.",
        request_body=CustomUserSerializer,
        responses={200: CustomUserSerializer, 400: "Bad Request", 404: "Not Found"},
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Actualiza parcialmente un usuario específico por ID.",
        request_body=CustomUserSerializer,
        responses={200: CustomUserSerializer, 400: "Bad Request", 404: "Not Found"},
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Elimina un usuario específico por ID.",
        responses={204: "No Content", 404: "Not Found"},
    ),
)
class CustomUserViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
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


class RegisterAPIView(generics.CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Registra los nuevos usuarios.",
        request_body=CustomUserSerializer,
        responses={201: CustomUserSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_description="Inician sesión los usuarios.",
        request_body=LoginSerializer,
        responses={200: "OK", 400: "Bad Request"},
    )
    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )
