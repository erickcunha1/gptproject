from database import mysql_connection

class PromptsInfo:
    def __init__(self, host, user, passwd, database=None) -> None:
        self.connection = mysql_connection(host, user, passwd, database)
        self.cursor = self.connection.cursor()

    PROMPT_TR_TITLES = {
        1: 'Termo de Referência',
        2: 'TR-Fundamentação da Contratação',
        3: 'TR- Descrição da solução como um todo considerado o ciclo de vida do objeto e especificação do produto',
        4: 'TR- Requisitos da Contratação'
    }

    TITULO_TR_TITLES = {
        1: "Condições Gerais da Contratação",
        2: "Fundamentação da Contratação",
        3: "Descrição da solução como um todo considerado o ciclo de vida do objeto e especificação do produto",
        4: "Requisitos da Contratação"
    }

    PROMPT_NAMES = {
        1: "descricao_objeto",
        2: "descricao_justificativa",
        3: "descricao_previsao_contratacao",
        4: "descricao_justificativa_quantidade",
        5: "prompt_estimativa_valor",
        6: "prompt_fundamentacao_legal",
        7: "prompt_justificativa_parcelamento",
        8: "prompt_pocicionamento_conclusivo",
    }

    TITULO_NAMES = {
        1: "Objeto",
        2: "Justificativa da necessidade da contratação, considerado o problema a ser resolvido sob a perspectiva do interesse público",
        3: "Demonstração da previsão da contratação",
        4: "Estimativas e Justificativas das quantidades para a contratação",
        5: "Estimativa de valor",
        6: "Fundamentação Legal",
        7: "Justificativa Parcelamento",
        8: "Posicionamento Conclusivo",
    }

    @staticmethod
    def get_prompt_tr(number):
        return PromptsInfo.PROMPT_TR_TITLES.get(number, 'Desconhecido')

    @staticmethod
    def get_titulo_tr(number):
        return PromptsInfo.TITULO_TR_TITLES.get(number, 'Desconhecido')

    @staticmethod
    def get_prompt_name(prompt_number):
        return PromptsInfo.PROMPT_NAMES.get(prompt_number, 'Desconhecido')

    @staticmethod
    def get_titulo_name(titulo_number):
        return PromptsInfo.TITULO_NAMES.get(titulo_number, 'Desconhecido')