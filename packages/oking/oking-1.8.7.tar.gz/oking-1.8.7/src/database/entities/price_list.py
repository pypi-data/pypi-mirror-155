
class DbPriceList:
    def __init__(self, ativo, codigo_filial, codigo_lista_preco, data_final, data_inicial, descricao_lista_preco, prioridade, tipo_escopo, cliente_erp):
        self.active: bool = ativo
        self.branch_code: str = codigo_filial
        self.price_list_code: str = codigo_lista_preco
        self.final_date: str = data_final
        self.initial_date: str = data_inicial
        self.price_list_description: str = descricao_lista_preco
        self.priority: int = prioridade
        self.scope_type: int = tipo_escopo
        self.client_code: str = cliente_erp


class PriceListProduct:
    def __init__(self, codigo_lista_preco, codigo_erp, preco_atual, preco_lista, preco_outro):
        self.price_list_code: str = codigo_lista_preco
        self.erp_code: str = codigo_erp
        self.price: float = preco_atual
        self.price_from: float = preco_lista
        self.other_price: float = preco_outro
