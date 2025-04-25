# feml/cli.py
import os
import shutil
import subprocess
import json
import yaml
import requests
import typer
from typing import Optional
from cookiecutter.main import cookiecutter

app = typer.Typer()
template_app = typer.Typer()
list_app = typer.Typer()
app.add_typer(template_app, name="template", help="Trabalhar com templates")
app.add_typer(list_app, name="list", help="Listar recursos")

USUARIO_PADRAO = "ntsation"  # <- Coloque seu nome de usuário GitHub aqui

@list_app.command("repos")
def listar_repositorios():
    """
    Lista repositórios do GitHub do usuário definido.
    """
    url = f"https://api.github.com/users/{USUARIO_PADRAO}/repos"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        repos = resposta.json()
        for repo in repos:
            print(f"📁 {repo['name']}")
    else:
        print(f"❌ Erro ao buscar repositórios: {resposta.status_code}")

@template_app.command("run")
def rodar_template(repo: str):
    """
    Executa um template cookiecutter de um repositório.
    """
    repo_url = f"https://github.com/{USUARIO_PADRAO}/{repo}.git"
    destino = f"./.cache/{repo}"
    perguntas_url = f"https://raw.githubusercontent.com/{USUARIO_PADRAO}/{repo}/main/perguntas.yaml"

    print(f"🔍 Verificando perguntas.yaml no repositório {repo}...")
    resposta = requests.get(perguntas_url)
    if resposta.status_code != 200:
        print("❌ Arquivo perguntas.yaml não encontrado no repositório (branch main).")
        raise typer.Exit(code=1)

    if os.path.exists(destino):
        shutil.rmtree(destino)

    print(f"🔄 Clonando {repo_url}...")
    subprocess.run(["git", "clone", repo_url, destino], check=True)

    perguntas_path = os.path.join(destino, "perguntas.yaml")
    print("📄 Lendo perguntas...")
    with open(perguntas_path, "r") as f:
        perguntas = yaml.safe_load(f)

    respostas = {}

    print("📝 Responda às perguntas:")
    for chave, dados in perguntas.items():
        prompt = dados.get("prompt", chave)
        default = dados.get("default", "")
        tipo = dados.get("type", "string")

        if default:
            valor = typer.prompt(f"{prompt}", default=default)
        else:
            valor = typer.prompt(f"{prompt}")

        if tipo == "int":
            valor = int(valor)
        elif tipo == "float":
            valor = float(valor)
        elif tipo == "bool":
            valor = valor.lower() in ["true", "1", "yes", "y"]

        respostas[chave] = valor

    cookiecutter_json_path = os.path.join(destino, "template", "cookiecutter.json")
    print("🧩 Gerando cookiecutter.json...")
    with open(cookiecutter_json_path, "w") as f:
        json.dump(respostas, f, indent=2)

    print("🚀 Rodando cookiecutter...")
    cookiecutter(os.path.join(destino, "template"))

if __name__ == "__main__":
    app()
