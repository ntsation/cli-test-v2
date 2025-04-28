import os
import requests
import yaml
import typer

def token_github() -> str:
    gh_config_path = os.path.expanduser("~/.config/gh/hosts.yml")

    if not os.path.exists(gh_config_path):
        raise typer.BadParameter("Execute `gh auth login` primeiro.")

    with open(gh_config_path, "r") as file:
        config = yaml.safe_load(file)

    github_info = config.get("github.com")
    if not github_info or "oauth_token" not in github_info:
        raise typer.BadParameter("Token OAuth não encontrado.")

    return github_info["oauth_token"]

def repositorios_user(user: str) -> list:
    token = token_github()
    url = f"https://api.github.com/users/{user}/repos?per_page=100&type=all"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    resposta = requests.get(url, headers=headers)
    if resposta.status_code != 200:
        raise typer.BadParameter(f"Erro ao buscar repositórios do usuário: {resposta.status_code} - {resposta.text}")

    return resposta.json()

def repositorios_org(org: str) -> list:
    token = token_github()
    url = f"https://api.github.com/orgs/{org}/repos?per_page=100&type=all"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    resposta = requests.get(url, headers=headers)
    if resposta.status_code != 200:
        raise typer.BadParameter(f"Erro ao buscar repositórios da organização: {resposta.status_code} - {resposta.text}")

    return resposta.json()
