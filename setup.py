# setup.py
from setuptools import setup, find_packages

setup(
    name="feml",
    version="0.1.0",
    description="CLI para GitHub e templates",
    author="Seu Nome",
    author_email="seu.email@dominio.com",
    packages=find_packages(),
    install_requires=[
        "typer",
        "cookiecutter",
        "requests",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "feml = feml.cli:app",  # Comando 'feml' no terminal chama 'cli.py'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
