# clarolib - Evoluindo a Biblioteca de validação de dados

## Pré Requisitos

- Python 3.x
- Docker e Docker Compose

## Introdução

O objetivo desse documento é descrever os passos para criação do ambiente de desenvolvimento da biblioteca **Clarolib**.

Essa biblioteca foi criada com os seguintes objetivos:
- Padronizar a etapa de validação das fontes de dados a serem ingeridas no *Datalake*
- Padronizar métricas e implementações de [linhagem de dados](https://docs.microsoft.com/pt-br/power-bi/collaborate-share/service-data-lineage)
- Dar mais agilidade/produtividade na criação de esteiras de validações de dados antes que esses sejam ingeridos no *Datalake*
- Evitar necessidade de repetição de códigos e deixar o código 'mais limpo'.

Abaixo estão os passos para criação do ambiente de desenvolvimento:

# Criação de [Ambiente Virtual Python](https://docs.python.org/pt-br/3/tutorial/venv.html)

Para criar o ambiente virtual, execute os comandos abaixo:
```sh
python3 -m venv clarolib_env
source clarolib_env/bin/activate

pip install -r requirements.txt
```

### **Executando o Apache Spark localmente com Docker**

Acesse a pasta `spark` folder no seu terminal e execute o comando abaixo.
Esse será responsável por iniciar a execução do spark localmente.

```sh
docker-compose up
```

### **Como executar exemplos localmente**

Acesse os arquivos de exemplo localizados no diretório `code_examples` e execute-os.

### **Desativando o ambiente virtual**

Acesse o diretorio `clarolib_env` e execute o seguinte comando:

```sh
deactivate
```

### **Compilando e executando testes unitários**

Para compilar os códigos, disparar a execução dos testes unitários e validação de [*code lint*](https://en.wikipedia.org/wiki/Lint_(software)) execute os passos conforme abaixo:

```sh
flake8 ./lib ./code_examples ./tests
pytest --ignore=setup.py
python3 setup.py sdist bdist_wheel
```
> Esses mesmos passos serão executados pela esteira do Azure Devops para garantir que os critérios mínimos de qualidade estão sendo seguidos.
> 
> Caso o código criado não esteja de acordo, a esteira **não** permitirá que esse código seja entregue.
