from database import mysql_connection


class PromptsInfo:
    def __init__(self, host, user, passwd, database=None) -> None:
        mysql_connection(host, user, passwd, database)
        self.connection = self.mysql_connection(host, user, passwd, database)
        self.cursor = self.connection.cursor()

    @staticmethod
    def get_prompt_tr(number):
        titulo_names = {
            1: 'Termo de Referência',
            2: 'TR-Fundamentação da Contratação',
            3: 'TR- Descrição da solução como um todo considerado o ciclo de vida do objeto e especificação do produto',
            4: 'TR- Requisitos da Contratação'
        }
        return titulo_names.get(number, 'Desconhecido')

    @staticmethod
    def get_titulo_tr(number):
        titulo_name = {
            1: "Condições Gerais da Contratação",
            2: "Fundamentação da Contratação",
            3: "Descrição da solução como um todo considerado o ciclo de vida do objeto e especificação do produto",
            4: "Requisitos da Contratação"
        }
        return titulo_name.get(number, 'Desconhecido')

    @staticmethod
    def get_prompt_name(prompt_number):
        prompt_names = {
            1: "descricao_objeto",
            2: "descricao_justificativa",
            3: "descricao_previsao_contratacao",
            4: "descricao_justificativa_quantidade",
            5: "prompt_estimativa_valor",
            6: "prompt_fundamentacao_legal",
            7: "prompt_justificativa_parcelamento",
            8: "prompt_pocicionamento_conclusivo",
        }
        return prompt_names.get(prompt_number, 'Desconhecido')

    @staticmethod
    def get_titulo_name(titulo_number):
        titulo_names = {
            1: "Objeto",
            2: "Justificativa da necessidade da contratação, considerado o problema a ser resolvido sob a perspectiva do interesse público",
            3: "Demonstração da previsão da contratação",
            4: "Estimativas e Justificativas das quantidades para a contratação",
            5: "Estimativa de valor",
            6: "Fundamentação Legal",
            7: "Justificativa Parcelamento",
            8: "Posicionamento Conclusivo",
        }
        return titulo_names.get(titulo_number, 'Desconhecido')
