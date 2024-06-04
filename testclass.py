
import re

def substituir_descricao_objeto(texto):
   
    padrao_1 = r"(Descrição do objeto:).*?\."
    texto = re.sub(padrao_1, r'\1$', texto, flags=re.DOTALL)

    # Substitui o trecho entre "1.3. O objeto desta contratação," e "não se enquadra"
    padrao_2 = r"(1\.3\ O objeto desta contratação,).*?(não se enquadra)"
    texto = re.sub(padrao_2, r'\1$\2', texto, flags=re.DOTALL)

    return texto




def substituir_objeto_contratacao(texto):
    """
    Substitui tudo entre "1.3. O objeto desta contratação," e "não se enquadra" por "$".

    Args:
    texto (str): O texto original.

    Returns:
    str: O texto com o trecho substituído por "$".
    """
    padrao = r"(1\.3\. O objeto desta contratação,).*?não se enquadra"
    texto = re.sub(padrao, r'\1$', texto, flags=re.DOTALL)
    return texto

def substituir_criterios_sustentabilidade(texto):
    """
    Substitui tudo entre "4.1  Além dos critérios de sustentabilidade eventualmente inseridos na descrição do objeto" e "outros critérios que também devem ser atendidos" por "$".

    Args:
    texto (str): O texto original.

    Returns:
    str: O texto com o trecho substituído por "$".
    """
    padrao = r"(4\.1  Além dos critérios de sustentabilidade eventualmente inseridos na descrição do objeto).*?outros critérios que também devem ser atendidos"
    texto = re.sub(padrao, r'\1$', texto, flags=re.DOTALL)
    return texto

def substituir_apos_451_ate_46(texto):
    """
    Substitui tudo após "4.5.1" até "4.6" por "$".

    Args:
    texto (str): O texto original.

    Returns:
    str: O texto com o trecho substituído por "$".
    """
    padrao = r"(4\.5\.1).*?4\.6"
    texto = re.sub(padrao, r'\1$', texto, flags=re.DOTALL)
    return texto


texto = """Descrição do Objeto
1.1 Descricao do objeto: WEBCAM, para videoconferencia, resolucao de video Full HD 1080p, campo de visao minima de 90°.

1.2 Os bens objeto desta contratacao sao caracterizados como comuns, conforme justificativa constante do Estudo Tecnico Preliminar.

1.3 O objeto desta contratacao, WEBCAM, para videoconferencia, resolucao de video Full HD 1080p, campo de visao minima de 90°, nao se enquadra como sendo de bem de luxo, conforme Decreto no 10.818, de 27 de setembro de 2021.

1.4 O prazo de vigencia da contratacao e de .............................. contados do(a) ............................., na forma do artigo 105 da Lei n° 14.133, de 2021.

1.5 O prazo de vigencia da contratacao e de .............................. (maximo de 5 anos) contados do(a) ............................., prorrogavel por ate 10 anos, na forma dos artigos 106 e 107 da Lei n° 14.133, de 2021.

1.5.1 O fornecimento de bens e enquadrado como continuado conforme definido no Estudo Tecnico Preliminar.

1.6 O contrato oferece maior detalhamento das regras que serao aplicadas em relacao a vigencia da contratacao.
Justificativa para Contratação
2.1 - A fundamentacao da contratacao e de seus quantitativos encontra-se pormenorizada em topico especifico do Estudo Tecnico Preliminar, apendice deste Termo de Referencia.
Solução Proposta
3.1. A descricao da solucao como um todo esta detalhada em um topico especifico do Estudo Tecnico Preliminar, que e um apendice deste Termo de Referencia.
Requisitos para Contratação
Quebrar paragrafo 
4.1 Alem dos criterios de sustentabilidade eventualmente inseridos na descricao do objeto, WEBCAM, para videoconferencia, resolucao de video Full HD 1080p, campo de visao minima de 90o outros criterios que tambem devem ser atendidos, que se baseiam no Guia Nacional de Contratacoes Sustentaveis. Sao eles: (listar 15 criterios). 

Quebrar paragrafo 
4.2 Na presente contratacao sera admitida a indicacao da(s) seguinte(s) marca(s), caracteristica(s) ou modelo(s), de acordo com as justificativas contidas no Estudo Tecnico Preliminar: (...).

Quebrar paragrafo 
Da vedacao de contratacao de marca ou produto: 

Quebrar paragrafo 
4.3. Diante das conclusoes extraidas do processo n. ____, a Administracao nao aceitara o fornecimento dos seguintes produtos/marcas:

Quebrar paragrafo 
4.3.1. ...
4.3.2. ...
4.3.3. ..

Da exigencia de amostra: 
4.4 Havendo o aceite da proposta quanto ao valor, o interessado classificado provisoriamente em primeiro lugar devera apresentar amostra, que tera data, local e horario de sua realizacao divulgados por mensagem no sistema, cuja presenca sera facultada a todos os interessados, incluindo os demais fornecedores interessados.

4.5 Serao exigidas amostras dos seguintes itens:
4.5.1.WEBCAM, para videoconferencia, resolucao de video Full HD 1080p, campo de visao minima de 90o

4.6. As amostras poderao ser entregues no endereco ____ , no prazo limite de _____, sendo que a empresa assume total responsabilidade pelo envio e por eventual atraso na entrega.
"""
if __name__ == '__main__':
    print(substituir_descricao_objeto(texto))