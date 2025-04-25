"""
Comandos para trabalhar com templates.
"""
import typer
from feml.config import USUARIO_PADRAO
from feml.cli.utils.template import (
    preparar_diretorio_template,
    carregar_perguntas_yaml,
    coletar_respostas,
    executar_cookiecutter
)

app = typer.Typer(help="Trabalhar com templates")


@app.command("run")
def rodar_template(
    repo: str = typer.Argument(..., help="Nome do repositório contendo o template"),
    nome_usuario: str = typer.Option(USUARIO_PADRAO, help="Nome de usuário do GitHub")
):
    """Executa um template cookiecutter de um repositório."""
    try:
        # Verificar e obter o template
        destino = preparar_diretorio_template(repo, nome_usuario)
        
        # Carregar perguntas
        perguntas = carregar_perguntas_yaml(destino)
        
        # Obter respostas do usuário
        respostas = coletar_respostas(perguntas)
        
        # Executar cookiecutter
        executar_cookiecutter(destino, respostas)
        
        print("✅ Execução do template concluída com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        raise typer.Exit(code=1)