import typer
from .config import USUARIO_PADRAO
from .github import repositorios_user, repositorios_org
from .cookie import diretorio, perguntas, respostas, run_cookie

app = typer.Typer(help="Ferramenta CLI FEML")
repos_app = typer.Typer()
app.add_typer(repos_app, name="repos")

@repos_app.command("user")
def listar_repositorios_user(user: str = typer.Option(USUARIO_PADRAO, help="Nome de usuário do GitHub")):
    """Lista repositórios públicos de um usuário do GitHub."""
    try:
        repos = repositorios_user(user)
        for repo in repos:
            print(f"-> {repo['name']}")
    except Exception as e:
        print(f"Erro: {e}")

@repos_app.command("org")
def listar_repositorios_org(org: str = typer.Argument(..., help="Nome da organização do GitHub")):
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
    app()

if __name__ == "__main__":
    main()
