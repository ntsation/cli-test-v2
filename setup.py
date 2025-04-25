from setuptools import setup, find_packages
import pathlib

# Caminho para o README.md (opcional)
here = pathlib.Path(__file__).parent
long_description = (here / "README.md").read_text(encoding="utf-8") if (here / "README.md").exists() else ""

setup(
    name="feml",
    version="0.1.0",
    description="CLI para trabalhar com templates do GitHub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nathan T. S.",
    author_email="nathan@email.com",
    url="https://github.com/ntsation/feml",  # ajuste se necessário
    packages=find_packages(),
    install_requires=[
        "typer[all]>=0.9",
        "cookiecutter",
        "requests",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "feml = feml.cli:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
