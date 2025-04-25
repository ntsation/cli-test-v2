"""
Ponto de entrada principal para o CLI FEML.
"""
import typer
from feml.cli.commands import list_commands, template_commands

# Aplicação principal
app = typer.Typer(help="Ferramenta CLI FEML")

# Registrar subcomandos
app.add_typer(template_commands.app, name="template", help="Trabalhar com templates")
app.add_typer(list_commands.app, name="list", help="Listar recursos")


def main():
    """Função principal para iniciar o CLI."""
    app()


if __name__ == "__main__":
    main()