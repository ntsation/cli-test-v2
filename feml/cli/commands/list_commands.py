"""
Comandos para listar recursos.
"""
import typer
from feml.config import USUARIO_PADRAO
from feml.cli.utils.github import obter_repositorios_github

app = typer.Typer(help="Listar recursos disponíveis")


@app.command("repos")
def listar_repositorios(
    nome_usuario: str = typer.Option(USUARIO_PADRAO, help="Nome de usuário do GitHub")
):
    """Lista repositórios do GitHub para o usuário especificado."""
    try:
        repos = obter_repositorios_github(nome_usuario)
        print(f"Encontrados {len(repos)} repositórios para o usuário {nome_usuario}:")
        for repo in repos:
            print(f"📁 {repo['name']}")
    except Exception as e:
        print(f"❌ Erro: {e}")