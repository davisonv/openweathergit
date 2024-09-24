# OpenWeatherGit

O projeto tem como objetivo oferecer uma camada de abstração para comunicar o 
OpenWeatherMap API com as gists do Github.

## Índice

- [Introdução](#introdução)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Uso](#uso)

## Introdução

O projeto tem como objetivo oferecer uma camada de abstração para comunicar o 
OpenWeatherMap API com as gists do Github. A estrutura do projeto é a seguinte:
    
        |.
        ├── Dockerfile
        ├── README.md
        ├── app
        │   ├── __init__.py
        │   ├── app.py
        │   ├── openweathersdk
        │   │   ├── __init__.py
        │   │   └── openweather.py
        │   ├── schemas.py
        │   └── util.py
        ├── docker-compose.yaml
        ├── poetry.lock
        ├── pyproject.toml
        └── tests
            ├── __init__.py
            ├── conftest.py
            ├── mocks.py
            ├── test_api.py
            ├── test_openweathersdk.py
            └── test_util.py

## Tecnologias Utilizadas

As principais tecnologias, bibliotecas e frameworks do projeto são as seguintes:

- Python
- Pytest
- FastAPI
- Docker
- Pydantic
- PyGithub

## Instalação

Instruções sobre como instalar e configurar o projeto localmente. Inclua detalhes sobre dependências e ambiente de desenvolvimento. Exemplo:

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/openweathergit.git
    openweathergit
    ```

2. Crie um ambiente virtual (É recomendado o uso do `Poetry`):
    ```bash
      poetry shell
    ```

3. Instale as dependências:
    ```bash
    poetry install
    ```

4. Configure as variáveis de ambiente:
    - Crie um arquivo `.env` e adicione as variáveis necessárias.
    - Configure as variaveis no `docker-compose.yaml` caso deseje rodar em
    ambiente docker.

## Uso

Neste projeto foram configurados alguns scripts de atalho, todos podem ser
rodados com o comando `task`, por exemplo:

```bash
task format # Irá aplicar formatações de estilo no codigo.
```

```bash
task test # Irá rodar os tests do projeto.
```

```bash
task run # Irá rodar a api do projeto.
```

Todos scripts estão na seção `[tool.taskipy.tasks]` do `pyproject.toml`, novos
scripts também devem ser adicionados nessa seção do arquivo.

Para levantar o ambiente docker basta rodar o comando:

```bash
docker-compose up --build
```