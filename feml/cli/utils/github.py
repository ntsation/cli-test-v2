"""
Utilitários para interação com a API do GitHub.
"""
import requests
import typer
import yaml
import os

def obter_token_github_cli() -> str:
    """
    Obtém o token de autenticação lendo o arquivo de configuração do GitHub CLI.

    Returns:
        Token de autenticação do GitHub.

    Raises:
        typer.BadParameter: Se não for possível obter o token.
    """
    gh_config_path = os.path.expanduser("~/.config/gh/hosts.yml")

    if not os.path.exists(gh_config_path):
        raise typer.BadParameter("Arquivo de configuração do GitHub CLI não encontrado. Execute `gh auth login` primeiro.")

    try:
        with open(gh_config_path, "r") as file:
            config = yaml.safe_load(file)

        github_info = config.get("github.com")
        if not github_info or "oauth_token" not in github_info:
            raise typer.BadParameter("Token OAuth não encontrado no arquivo de configuração.")

        return github_info["oauth_token"]

    except Exception as e:
        raise typer.BadParameter(f"Erro ao ler o token do GitHub CLI: {e}")


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
    token = obter_token_github_cli()

    url = "https://api.github.com/user/repos?per_page=100&type=all"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    resposta = requests.get(url, headers=headers)
    
    if resposta.status_code != 200:
        raise typer.BadParameter(f"Erro ao buscar repositórios: {resposta.status_code}")
    
    return resposta.json()