# Minha API

Esta aplicacao tem o objetivo de manter um cadastro de despesas.
Foi utilizada a versao do Python 3.12.2

---
## Como executar 

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

```
python -m venv env  
```

```
env/Scripts/activate
```

```
(env)$ pip install -r requirements.txt
```

Para inicializar a API basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5001
```

Após a inicializacao do servidor, o arquivo db.sqlite3 será criado automaticamente com as duas tabelas do sistema.

Para carga inicial na tabela de tipo de despesas, deverao ser executado os passos abaixo:

Abra um novo terminal e navegue até a pasta raiz do projeto

Execute p comando abaixo para carga de inserts de tipo de despesas

Python script_insert_tipo_despesa.py

Certifique que a tabela tipo_despesa esteja devidamente populada no arquivo db.sqlite3

Abra o [http://localhost:5001/#/](http://localhost:5001/#/) no navegador para verificar se a aplicacao esta no ar.

## Como executar atraves do Docker

Certifique-se de ter o Docker instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal. Execute como administrador o seguinte comando para construir a imagem Docker:

$ docker build -t imagem-backend .   

Uma vez criada a imagem, para executar o container basta executar, como administrador, seguinte o comando:

$ docker run -p 5001:5001 imagem-backend
