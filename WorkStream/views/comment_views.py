from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import Http404, get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from WorkStream.models import Comment, Task
from WorkStream.permissions import IsCommentOwner
from WorkStream.serializers import CommentSerializer

User = get_user_model()


class CommentListAPIView(generics.ListAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Lista todos los comentarios",
        responses={200: CommentSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(operation_description="Creación de comentarios"),
)
class CommentCreateAPIView(generics.CreateAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        task_id = self.request.data.get("task")

        # Verificar si el task_id está presente en los datos
        if not task_id:
            raise ValidationError({"error": "Task ID is required"})

        try:
            task = get_object_or_404(Task, id=task_id)
        except Http404:
            raise ValidationError({"error": "Task does not exist"})
        except Exception as e:
            raise ValidationError({"error": str(e)})

        try:
            comment = serializer.save(user=self.request.user, task=task)
        except Exception as e:
            raise ValidationError({"error": str(e)})

        return comment

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            comment = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentOwner]
    lookup_url_kwarg = "comment_id"

    @swagger_auto_schema(
        operation_description="Trae un comentario según el id",
        responses={
            200: CommentSerializer,
            204: "No Content",
            403: "Forbidden",
            404: "Not Found",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza un comentario",
        request_body=CommentSerializer,
        responses={200: CommentSerializer, 400: "Bad Request", 403: "Forbidden"},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Elimina un comentario",
        responses={204: "No Content", 403: "Forbidden", 404: "Not Found"},
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Verifica si el usuario es el creador del comentario
        if instance.user != request.user:
            return Response(
                {"error": "No tienes permiso para eliminar este comentario."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Lógica personalizada antes de la eliminación
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):

        instance.delete()
