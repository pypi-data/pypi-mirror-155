from typing import List


class Escopo:
    def __init__(self, tipo_escopo: int, codigos_escopo: List[str]):
        self.tipo_escopo: int = tipo_escopo
        self.codigos_escopo: List[str] = codigos_escopo


class ListaPreco:
    def __init__(self, descricao_lista_preco: str, codigo_lista_preco: str, codigo_filial: str, data_inicial: str, data_final: str, ativo: bool, prioridade: int, escopo: Escopo):
        self.descricao_lista_preco: str = descricao_lista_preco
        self.codigo_lista_preco: str = codigo_lista_preco
        self.codigo_filial: str = codigo_filial
        self.data_inicial: str = data_inicial
        self.data_final: str = data_final
        self.ativo: bool = ativo
        self.prioridade: int = prioridade
        self.escopo: Escopo = escopo


class ListaPrecoResponse:
    def __init__(self, Identifiers, Status, Message, Protocolo):
        self.identifiers: List[str] = Identifiers
        self.status: int = Status
        self.message: str = Message
        self.protocol: str = Protocolo
