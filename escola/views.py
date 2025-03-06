from escola.models import Estudante, Curso, Matricula
from escola.serializers import (
    EstudanteSerializer,
    CursoSerializer,
    MatriculaSerializer,
    ListaMatriculasEstudanteSerializer,
    ListaMatriculasCursoSerializer,
    EstudanteSerializerV2,
)
from rest_framework import viewsets, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import UserRateThrottle
from .throttles import MatriculaAnonRateThrottle
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class EstudanteViewSet(viewsets.ModelViewSet):
    """
    - Endpoint para CRUD de estudantes.

    Ordenação
    - nome: permite order os resultados por nome.

    Pesquisa
    - nome: permite pesquisar por nome.
    - cpf: permite pesquisar por CPF.

    Metodos HTTP Permitidos:
    - GET, POST, PUT, DELETE, PATCH

    Serializer
    - EstudanteSerializer: usado para serialização e desserialização de dados.
    - Se a versão da API for 'v2', usa EstudanteSerializerV2
    """
    queryset = Estudante.objects.all().order_by("id")
    # serializer_class = EstudanteSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["nome"]
    search_fields = ["nome", "cpf"]

    def get_serializer_class(self):
        if self.request.version == "v2":
            return EstudanteSerializerV2
        return EstudanteSerializer


class CursoViewSet(viewsets.ModelViewSet):
    """
    - Endpoint para CRUD de cursos.

    HTTP permitidos:
    - GET, POST, PUT, DELETE, PATCH
    """
    queryset = Curso.objects.all().order_by("id")
    serializer_class = CursoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MatriculaViewSet(viewsets.ModelViewSet):
    """
    Descrição da ViewSet:
    - Endpoint para CRUD de matrículas

    Métodos HTTP Permitidos:
    - GET, POST

    Throttle Classes:
    - MatriculaAnonRateThrottle: limite de taxa para usuários anônimos.
    - UserRateThrottle: limite de taxa para usuários autenticados.
    """
    queryset = Matricula.objects.all().order_by("id")
    serializer_class = MatriculaSerializer
    throttle_classes = [UserRateThrottle, MatriculaAnonRateThrottle]
    http_method_names = ["get", "post"]


class ListaMatriculaEstudante(generics.ListAPIView):
    """
    Descrição da View:
    - Lista Matriculas por id de Estudante
    Parâmetros:
    - pk (int): O identificador primário do objeto deve ser um número inteiro.
    """

    def get_queryset(self):
        estudante_id = self.kwargs["pk"]
        return Matricula.objects.filter(estudante_id=estudante_id).order_by("id")

    serializer_class = ListaMatriculasEstudanteSerializer


class ListaMatriculaCurso(generics.ListAPIView):
    """
    Descrição da View:
    - Lista Matriculas por id de Curso
    Parâmetros:
    - pk (int): O identificador primário do objeto deve ser um número inteiro.
    """

    def get_queryset(self):
        queryset = Matricula.objects.filter(cursoid=self.kwargs["pk"]).order_by("id")
        return queryset

    serializer_class = ListaMatriculasCursoSerializer
