import shutil
import yaml
import typer
from pathlib import Path
from typing import Dict, Any
import git
from cookiecutter.main import cookiecutter
from .config import DIRETORIO_CACHE

def diretorio(repo: str, nome_usuario: str) -> Path:
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
    perguntas = template_path / "cookiecutter.yaml"
    if not perguntas.exists():
        raise FileNotFoundError("Arquivo cookiecutter.yaml não encontrado")
    
    with open(perguntas, "r") as f:
        return yaml.safe_load(f)

def respostas(perguntas: Dict[str, Any]) -> Dict[str, Any]:
    respostas = {}
    for chave, dados in perguntas.items():
        prompt = dados.get("prompt", chave)
        padrao = dados.get("default", "")
        tipo_valor = dados.get("type", "string")
        
        valor = typer.prompt(prompt, default=padrao) if padrao else typer.prompt(prompt)
        
        if tipo_valor == "int":
            valor = int(valor)
        elif tipo_valor == "float":
            valor = float(valor)
        elif tipo_valor == "bool":
            valor = valor.lower() in ["true", "1", "yes", "y", "sim", "s"]
        
        respostas[chave] = valor
    return respostas

def run_cookie(template_path: Path, respostas: Dict[str, Any]) -> None:
    print("🚀 Executando cookiecutter...")
    cookiecutter(str(template_path), no_input=True, extra_context=respostas)
