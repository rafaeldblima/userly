## Userly
Uma API para usuários.

## Index
- [Dependências](#dependências)
- [Pipenv](#pipenv)
- [Docker](#docker)
- [Makefile](#makefile)
- [Httpie](#httpie)


### Dependências

* Python 3.8.x
* Pipenv - Gerenciador de pacotes Python - [Docs](https://docs.pipenv.org)

`export FLASK_APP=api.py`


### Como subir o ambiente?
Você pode utilizar pipenv or docker. 
 
#### Pipenv
1. Crie seu ambiente

```bash
pipenv --python 3.8
```
2.  Instale os pré-requisitos
```bash
pipenv install
```
**Observação**: Dependências de desenvolvimento(teste, lint, etc) tem que ser
 instaladas com o comando `pipenv install --dev`.
 
3. Utilize o comando abaixo para rodar a API: 
```bash
pipenv shell
make run
```
4. No navegador acesse: http://127.0.0.1:5000/

#### Docker 
1. Ter instalado docker e docker-compose

2. Suba os containers
```bash
docker-compose up -d
```
3. No navegador acesse: http://127.0.0.1:8000/

## Makefile
#### Comandos
**Importante:** Necessário estar dentro do ambiente criado pelo pipenv (`pipenv shell`)
```bash
make <comando>
```
- run: Subir api
- test: Rodar testes
- coverage: Rodar testes com coverage

#### Httpie
##### Testar requests com auth (instalar dependências de dev antes)
```virtualenv
http --json --auth <email>:<password> GET  http://127.0.0.1:5000/api/v1/users/1
```
```virtualenv
http --auth <email>:<password> --json POST http://127.0.0.1:5000/api/v1/tokens/
```