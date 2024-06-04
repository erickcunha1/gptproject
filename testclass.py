
import re

def substituir_descricao_objeto(texto):
    padrao_1 = r"(Descrição do objeto:).*?\."
    texto = re.sub(padrao_1, r'\1$', texto, flags=re.DOTALL)

    # Substitui o trecho entre "1.3. O objeto desta contratação," e "não se enquadra"
    padrao_2 = r"(1\.3\ O objeto desta contratação,).*?(não se enquadra)"
    texto = re.sub(padrao_2, r'\1$\2', texto, flags=re.DOTALL)

    return texto

def substituir_criterios_sustentabilidade(texto):
    padrao_1 = r"(4\.1 Além dos critérios de sustentabilidade eventualmente inseridos na descrição do objeto,).*?(outros critérios que também devem ser atendidos)"
    texto = re.sub(padrao_1, r'\1$', texto, flags=re.DOTALL)

    padrao_2 = r"(4\.5\.1\.).*?(4\.6)"
    texto = re.sub(padrao_2, r'\1$', texto, flags=re.DOTALL)
    return texto