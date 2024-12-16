from rest_framework import serializers
from escola.models import Estudante, Curso, Matricula
from escola.validators import cpf_invalido, celular_invalido, nome_invalido


class EstudanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = "__all__"

    def validate(self, dados):
        if cpf_invalido(dados["cpf"]):
            raise serializers.ValidationError({"cpf": "CPF deve ser válido"})
        if nome_invalido(dados["nome"]):
            raise serializers.ValidationError({"nome": "Nome só pode ter letras"})
        if celular_invalido(dados["cel"]):
            raise serializers.ValidationError({"cel": "Celular deve seguir o modelo: 00 00000-0000. Respeitando traços e espaços."})
        return dados


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = "__all__"


class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        exclude = []


class ListaMatriculasEstudanteSerializer(serializers.ModelSerializer):
    curso = serializers.ReadOnlyField(source="curso.descricao")
    periodo = serializers.SerializerMethodField()

    class Meta:
        model = Matricula
        fields = ["curso", "periodo"]

    def get_periodo(self, obj):
        return obj.get_periodo_display()


class ListaMatriculasCursoSerializer(serializers.ModelSerializer):
    estudante_nome = serializers.ReadOnlyField(source="estudante.nome")

    class Meta:
        model = Matricula
        fields = ["estudante_nome"]
