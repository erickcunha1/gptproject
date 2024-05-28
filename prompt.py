class PromptsInfo:
    
    COLUMN_TR_NAME = {
        1:  "descricao_objeto_tr",
        2:  "descricao_fundamentacao_contratacao",
        3:  "descricao_solucao",
        4:  "requisitos_contratacao",
        5:  "modelo_execucao_objeto",
        6:  "modelo_gestao_contrato",
        7:  "criterios_medicao_pagamento",
        8:  "criterios_selecao_fornecedor",
        9:  "estimativas_valor",
        10: "adequacao_orcamentaria",
    }

    TITLES_TR = {
        1:  "Descrição do Objeto",
        2:  "Justificativa para Contratação",
        3:  "Solução Proposta",
        4:  "Requisitos para Contratação",
        5:  "Modelo de Execução do Objeto",
        6:  "Modelo de Gestão do Contrato",
        7:  "Critérios de Medição e Pagamento",
        8:  "Critérios para Seleção de Fornecedores",
        9: "Estimativas de Custos",
        10: "Adequação Orçamentária",
    }

    COLUMN_ETP_NAME = {
        1: "descricao_objeto",
        2: "descricao_justificativa",
        3: "descricao_previsao_contratacao",
        4: "requisitos_contratacao",
        5: "descricao_justificativa_quantidade",
        6: "prompt_estimativa_valor",
        7: "prompt_fundamentacao_legal",
        8: "prompt_justificativa_parcelamento",
        9: "prompt_posicionamento_conclusivo",
    }

    TITLES_ETP = {
        1: "Objeto",
        2: "Justificativa da necessidade da contratação, considerado o problema a ser resolvido sob a perspectiva do interesse público",
        3: "Demonstração da previsão da contratação",
        4: "Requisitos para Contratação",
        5: "Estimativas e Justificativas das quantidades para a contratação",
        6: "Estimativa de valor",
        7: "Fundamentação Legal",
        8: "Justificativa Parcelamento",
        9: "Posicionamento Conclusivo",
    }

    @staticmethod
    def get_column_tr(number):
        return PromptsInfo.COLUMN_TR_NAME.get(number)

    @staticmethod
    def get_title_tr(number):
        return PromptsInfo.TITLES_TR.get(number)

    @staticmethod
    def get_column_etp(prompt_number):
        return PromptsInfo.COLUMN_ETP_NAME.get(prompt_number)

    @staticmethod
    def get_title_etp(titulo_number):
        return PromptsInfo.TITLES_ETP.get(titulo_number)