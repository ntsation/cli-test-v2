"""
Utilitários para interação com a API do GitHub.
"""
import requests
import typer


def obter_repositorios_github(nome_usuario: str) -> list:
    """
    Busca repositórios de um usuário do GitHub.
    
    Args:
        nome_usuario: Nome de usuário do GitHub
        
    Returns:
        Lista de repositórios do usuário
        
    Raises:
        typer.BadParameter: Se ocorrer um erro ao buscar os repositórios
    """
    url = f"https://api.github.com/users/{nome_usuario}/repos"
    resposta = requests.get(url)
    
    if resposta.status_code != 200:
        raise typer.BadParameter(f"Erro ao buscar repositórios: {resposta.status_code}")
    
    return resposta.json()