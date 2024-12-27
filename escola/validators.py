import re
from validate_docbr import CPF

def cpf_invalido(numero_cpf):
    cpf = CPF()
    cpf_valido = cpf.validate(numero_cpf)
    return not cpf_valido


def nome_invalido(nome):
    return not nome.isalpha()


def celular_invalido(celular):
    # refatorar regex para não precisar digitar espaço e caractere especial
    modelo = "[0-9]{2} [0-9]{5}-[0-9]{4}"
    resposta = re.findall(modelo, celular)
    print(resposta)
    return not resposta
