from escola.models import Estudante, Curso, Matricula
from escola.serializers import (
    EstudanteSerializer,
    CursoSerializer,
    MatriculaSerializer,
    ListaMatriculasEstudanteSerializer,
    ListaMatriculasCursoSerializer,
    EstudanteSerializerV2
)
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from rest_framework import viewsets, generics, filters
from django_filters.rest_framework import DjangoFilterBackend


class EstudanteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Estudante.objects.all()
    # serializer_class = EstudanteSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["nome"]
    search_fields = ["nome", "cpf"]
    def get_serializer_class(self):
        if self.request.version == 'v2':
            return EstudanteSerializerV2
        return EstudanteSerializer


class CursoViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:  # Apenas leitura
            return [permission() for permission in [IsAuthenticatedOrReadOnly]]
        return [permission() for permission in [IsAdminUser]]

    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer


class ListaMatriculaEstudante(generics.ListAPIView):
    def get_queryset(self):
        estudante_id = self.kwargs["pk"]
        return Matricula.objects.filter(estudante_id=estudante_id)

    serializer_class = ListaMatriculasEstudanteSerializer


class ListaMatriculaCurso(generics.ListAPIView):

    def get_queryset(self):
        queryset = Matricula.objects.filter(cursoid=self.kwargs["pk"])
        return queryset

    serializer_class = ListaMatriculasCursoSerializer
