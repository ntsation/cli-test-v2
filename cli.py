import requests
import typer
import yaml
import os
import shutil
import git
import yaml
import typer
from pathlib import Path
from typing import Dict, Any
from cookiecutter.main import cookiecutter
from feml.config import DIRETORIO_CACHE


USUARIO_PADRAO = "ntsation"
DIRETORIO_CACHE = Path("./.cache")
DIRETORIO_CACHE.mkdir(exist_ok=True)

app = typer.Typer(help="Ferramenta CLI FEML")

repos_app = typer.Typer()
app.add_typer(repos_app, name="repos")

def diretorio(repo: str, nome_usuario: str) -> Path:
    """
    Prepara o diretório para o template.
    """
    repo_url = f"https://github.com/{nome_usuario}/{repo}.git"
    destino = DIRETORIO_CACHE / repo
    
    if destino.exists():
        shutil.rmtree(destino)
    
    DIRETORIO_CACHE.mkdir(exist_ok=True)
    print(f"Clonando {repo_url}...")
    
    try:
        git.Repo.clone_from(repo_url, str(destino))
    except git.exc.GitCommandError as e:
        print(f"Erro ao clonar o repositório: {e}")
        raise typer.Exit(code=1)
    
    return destino

def perguntas(template_path: Path) -> Dict[str, Any]:
    """
    Carrega e valida o arquivo YAML de perguntas.
    """
    perguntas = template_path / "cookiecutter.yaml"
    
    if not perguntas.exists():
        print("Arquivo cookiecutter.yaml não encontrado no repositório.")
        raise FileNotFoundError("Arquivo cookiecutter.yaml não encontrado")
    
    with open(perguntas, "r") as f:
        perguntas = yaml.safe_load(f)
    
    return perguntas

def respostas(perguntas: Dict[str, Any]) -> Dict[str, Any]:
    """
    Solicita ao usuário as respostas com base nas perguntas.
    """
    respostas = {}
    
    for chave, dados in perguntas.items():
        prompt = dados.get("prompt", chave)
        padrao = dados.get("default", "")
        tipo_valor = dados.get("type", "string")
        
        valor = typer.prompt(f"{prompt}", default=padrao) if padrao else typer.prompt(f"{prompt}")
        
        if tipo_valor == "int":
            valor = int(valor)
        elif tipo_valor == "float":
            valor = float(valor)
        elif tipo_valor == "bool":
            valor = valor.lower() in ["true", "1", "yes", "y", "sim", "s"]
        
        respostas[chave] = valor
    
    return respostas

def run_cookie(template_path: Path, respostas: Dict[str, Any]) -> None:
    """
    Executa o cookiecutter com as respostas fornecidas.
    """
    print("🚀 Executando cookiecutter...")
    cookiecutter(
        str(template_path),
        no_input=True,
        extra_context=respostas
    )

def token_github() -> str:
    """
    Obtém o token de autenticação lendo o arquivo de configuração do GitHub CLI.
    """
    gh_config_path = os.path.expanduser("~/.config/gh/hosts.yml")

    if not os.path.exists(gh_config_path):
        raise typer.BadParameter("Execute `gh auth login` primeiro.")

    try:
        with open(gh_config_path, "r") as file:
            config = yaml.safe_load(file)

        github_info = config.get("github.com")
        if not github_info or "oauth_token" not in github_info:
            raise typer.BadParameter("Token OAuth não encontrado no arquivo de configuração.")

        return github_info["oauth_token"]

    except Exception as e:
        raise typer.BadParameter(f"Erro ao ler o token do GitHub CLI: {e}")

def repositorios_user(user: str) -> list:
    token = token_github()

    url = "https://api.github.com/user/repos?per_page=100&type=all"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    resposta = requests.get(url, headers=headers)

    if resposta.status_code != 200:
        raise typer.BadParameter(f"Erro ao buscar repositórios do usuário autenticado: {resposta.status_code} - {resposta.text}")

    return resposta.json()

def repositorios_org(org: str) -> list:
    """
    Busca repositórios de uma organização do GitHub que o usuário autenticado tem acesso.
    """
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

@repos_app.command("user")
def listar_repositorios_user(
    user: str = typer.Option(USUARIO_PADRAO, help="Nome de usuário do GitHub")
):
    """Lista repositórios públicos de um usuário do GitHub."""
    try:
        repos = repositorios_user(user)
        for repo in repos:
            print(f"-> {repo['name']}")
    except Exception as e:
        print(f"Erro: {e}")

@repos_app.command("org")
def listar_repositorios_org(
    org: str = typer.Argument(..., help="Nome da organização do GitHub")
):
    """Lista repositórios públicos de uma organização do GitHub."""
    try:
        repos = repositorios_org(org)
        for repo in repos:
            print(f"-> {repo['name']}")
    except Exception as e:
        print(f"Erro: {e}")

@app.command("run")
def run(
    repo: str = typer.Argument(..., help="Nome do repositório contendo o template"),
    user: str = typer.Option(USUARIO_PADRAO, help="Nome de usuário do GitHub")
):
    """Executa um template cookiecutter de um repositório."""
    try:
        destino = diretorio(repo, user)
        
        perguntas_dict = perguntas(destino)
        
        respostas_dict = respostas(perguntas_dict)
        
        run_cookie(destino, respostas_dict)
        
        print("Execução do template concluída com sucesso!")
        
    except Exception as e:
        print(f"Erro: {e}")
        raise typer.Exit(code=1)
 
def main():
    """Função principal para iniciar o CLI."""
    app()

if __name__ == "__main__":
    main()