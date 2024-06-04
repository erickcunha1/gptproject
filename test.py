
import re

# Texto de exemplo
texto = """1.1 Descrição do objeto: XICARA, para chá, com pires, em porcelana, lisa, na cor branca, capacidade 200 ml.

1.2 Os bens objeto desta contratação são caracterizados como comuns, conforme justificativa constante do Estudo Técnico Preliminar."""

# Expressão regular
regex = r"(Descrição do objeto:).*?\."

# Substituição
resultado = re.sub(regex, r'\1$', texto)

print(resultado)