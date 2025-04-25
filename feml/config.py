"""
Configurações globais para o projeto FEML.
"""
from pathlib import Path

# Configurações do usuário
USUARIO_PADRAO = "ntsation"  # <- Nome de usuário do GitHub

# Configurações de diretórios
DIRETORIO_CACHE = Path("./.cache")

# Garantir que o diretório de cache exista
DIRETORIO_CACHE.mkdir(exist_ok=True)