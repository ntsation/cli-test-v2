import typer
from .github import repositorios_user, repositorios_org
from .cookie import diretorio, perguntas, respostas, run_cookie
from typing import Optional

app = typer.Typer(help="Ferramenta CLI FEML")
repos_app = typer.Typer()
app.add_typer(repos_app, name="repos")

@repos_app.command("user")
def listar_repositorios_user(
    user: str
):
    """Lista repositórios públicos de um usuário."""
    try:
        repos = repositorios_user(user)
        for repo in repos:
            print(f"-> {repo['name']}")
    except Exception as e:
        print(f"Erro: {e}")

@repos_app.command("org")
def listar_repositorios_org(
    org: str
):
    """Lista repositórios públicos de uma organização."""
    try:
        repos = repositorios_org(org)
        for repo in repos:
            print(f"-> {repo['name']}")
    except Exception as e:
        print(f"Erro: {e}")

@app.command("run")
def run(
    repo: str = typer.Argument(..., help="Nome do repositório contendo o template"),
    org: Optional[str] = typer.Option(None, "--org", "-o", help="Nome da organização do GitHub"),
    user: Optional[str] = typer.Option(None, "--user", "-u", help="Nome do usuário do GitHub"),
):
    """Executa um template cookiecutter de um repositório."""
    try:
        if org:
            destino = diretorio(repo, org)
        elif user:
            destino = diretorio(repo, user)
        else:
            raise ValueError("Você deve especificar uma organização ou um usuário (--org ou --user).")
        
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
