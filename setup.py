"""
Script de instalação para o pacote FEML.
"""
from setuptools import setup, find_packages

setup(
    name="feml",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer[all]",
        "cookiecutter",
        "requests",
        "PyYAML",
    ],
    entry_points="""
        [console_scripts]
        feml=feml.cli.main:main
    """,
    author="Seu Nome",
    author_email="seu.email@exemplo.com",
    description="Ferramenta CLI para gerenciar templates e recursos",
    keywords="cli, template, github",
    python_requires=">=3.7",
)