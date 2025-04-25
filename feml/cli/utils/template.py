"""
Utilitários para trabalhar com templates.
"""
import shutil
import subprocess
import yaml
import typer
from pathlib import Path
from typing import Dict, Any
from cookiecutter.main import cookiecutter
from feml.config import DIRETORIO_CACHE


def preparar_diretorio_template(repo: str, nome_usuario: str) -> Path:
    """
    Prepara o diretório para o template.
    
    Args:
        repo: Nome do repositório
        nome_usuario: Nome de usuário do GitHub
        
    Returns:
        Caminho para o diretório do template clonado
    """
    repo_url = f"https://github.com/{nome_usuario}/{repo}.git"
    destino = DIRETORIO_CACHE / repo
    
    # Limpar diretório existente se houver
    if destino.exists():
        shutil.rmtree(destino)
    
    # Criar diretório de cache se não existir
    DIRETORIO_CACHE.mkdir(exist_ok=True)
    
    # Clonar o repositório
    print(f"🔄 Clonando {repo_url}...")
    subprocess.run(["git", "clone", repo_url, str(destino)], check=True)
    
    return destino


def carregar_perguntas_yaml(diretorio_template: Path) -> Dict[str, Any]:
    """
    Carrega e valida o arquivo YAML de perguntas.
    
    Args:
        diretorio_template: Caminho para o diretório do template
        
    Returns:
        Dicionário com as perguntas carregadas
        
    Raises:
        FileNotFoundError: Se o arquivo cookiecutter.yaml não for encontrado
    """
    caminho_perguntas = diretorio_template / "cookiecutter.yaml"
    print("📄 Lendo perguntas...")
    
    if not caminho_perguntas.exists():
        print("❌ Arquivo cookiecutter.yaml não encontrado no repositório.")
        raise FileNotFoundError("Arquivo cookiecutter.yaml não encontrado")
    
    with open(caminho_perguntas, "r") as f:
        perguntas = yaml.safe_load(f)
    
    return perguntas


def coletar_respostas(perguntas: Dict[str, Any]) -> Dict[str, Any]:
    """
    Solicita ao usuário as respostas com base nas perguntas.
    
    Args:
        perguntas: Dicionário com as perguntas
        
    Returns:
        Dicionário com as respostas do usuário
    """
    respostas = {}
    
    print("📝 Por favor, responda às perguntas:")
    for chave, dados in perguntas.items():
        prompt = dados.get("prompt", chave)
        padrao = dados.get("default", "")
        tipo_valor = dados.get("type", "string")
        
        # Obter entrada do usuário
        valor = typer.prompt(f"{prompt}", default=padrao) if padrao else typer.prompt(f"{prompt}")
        
        # Converter tipo se necessário
        if tipo_valor == "int":
            valor = int(valor)
        elif tipo_valor == "float":
            valor = float(valor)
        elif tipo_valor == "bool":
            valor = valor.lower() in ["true", "1", "yes", "y", "sim", "s"]
        
        respostas[chave] = valor
    
    return respostas


def executar_cookiecutter(diretorio_template: Path, respostas: Dict[str, Any]) -> None:
    """
    Executa o cookiecutter com as respostas fornecidas.
    
    Args:
        diretorio_template: Caminho para o diretório do template
        respostas: Dicionário com as respostas do usuário
    """
    print("🚀 Executando cookiecutter...")
    cookiecutter(
        str(diretorio_template),
        no_input=True,
        extra_context=respostas
    )