import shutil
import typer
from cookiecutter.main import cookiecutter

def run_cookie(repo: str, usuario: str) -> None:
    url = f"https://github.com/{usuario}/{repo}"

    try:
        cookiecutter(url)
    except Exception as e:
        typer.echo(f"Erro ao gerar o projeto: {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    typer.run(run_cookie)
