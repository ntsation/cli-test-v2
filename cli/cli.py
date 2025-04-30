import typer
from .github import repositorios_user, repositorios_org
from .cookie import diretorio, perguntas, respostas, run_cookie
from typing import Optional

app = typer.Typer(help="Ferramenta CLI FEML")
repos_app = typer.Typer()
list_app = typer.Typer()

repos_app.add_typer(list_app, name="list")
app.add_typer(repos_app, name="repos")

template_app = typer.Typer(help="Comandos relacionados a templates")
app.add_typer(template_app, name="template")

@list_app.command("user")
def listar_repositorios_user(
    user: str = typer.Option(None, "--user", "-u", help="Nome do usuário. Se omitido, lista repositórios do usuário autenticado.")
):
    try:
        repos = repositorios_user(user)
        if not repos:
            print("Nenhum repositório encontrado.")
        for repo in repos:
            print(f"-> {repo['name']}")
    except Exception as e:
        print(f"Erro: {e}")

@list_app.command("org")
def listar_repositorios_org(
    org: str
):
    try:
        repos = repositorios_org(org)
        for repo in repos:
            print(f"-> {repo['name']}")
    except Exception as e:
        print(f"Erro: {e}")


@template_app.command("run")
def run_template(
    repo: str = typer.Argument(..., help="Nome do repositório contendo o template"),
    org: Optional[str] = typer.Option(None, "--org", "-o", help="Nome da organização do GitHub"),
    user: Optional[str] = typer.Option(None, "--user", "-u", help="Nome do usuário do GitHub"),
):
    """Executa um template cookiecutter de um repositório."""
    try:
        if org and user:
            raise ValueError("Escolha apenas um entre --org e --user.")
        elif org:
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
