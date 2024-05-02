import sys
from cx_Freeze import setup, Executable

# Arquivo .env para incluir no build
# include_files = [
#     ".env",  # Ajuste o caminho conforme necessário
# ]

# Definindo o script principal
executables = [Executable("main.py", base="Win32GUI" if sys.platform == "win32" else None)]

# Dependências adicionais para incluir no build
packages = [
    "os",
    "PyQt5",
    "openai",
    "bcrypt",
    "mysql.connector",
    "docx",
    "datetime",
]

# Incluindo todos os módulos utilizados no projeto e o arquivo .env
options = {
    'build_exe': {
        'packages': packages,
        # 'include_files': include_files,  # Adiciona arquivos estáticos ao build
        'excludes': ['tkinter'],  # Exemplo de exclusão, se necessário
    },
}

# Informações de configuração
setup(
    name="MeuProjeto",
    version="0.1",
    description="Meu projeto feito com cx_Freeze",
    options=options,
    executables=executables,
)
