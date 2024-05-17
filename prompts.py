class PromptsInfo:
    
    PROMPT_TR_TITLES = {
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

    TITULO_TR_TITLES = {
        1:  "Descrição do Objeto",
        2:  "Justificativa para Contratação",
        3:  "Solução Proposta",
        4:  "Requisitos da Contratação",
        5:  "Requisitos para Contratação",
        6:  "Modelo de Execução do Objeto",
        7:  "Modelo de Gestão do Contrato",
        8:  "Critérios de Medição e Pagamento",
        9:  "Critérios para Seleção de Fornecedores",
        10: "Estimativas de Custos",
        11: "Adequação Orçamentária",
    }

    PROMPT_NAMES = {
        1: "descricao_objeto",
        2: "descricao_justificativa",
        3: "descricao_previsao_contratacao",
        4: "descricao_justificativa_quantidade",
        5: "prompt_estimativa_valor",
        6: "prompt_fundamentacao_legal",
        7: "prompt_justificativa_parcelamento",
        8: "prompt_posicionamento_conclusivo",
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