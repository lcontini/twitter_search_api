# Twitter Search Api

Este projeto destina-se a utilizar as APIs do Twitter para buscar os ultimos 100 tweets baseados em hashtags predefinidas, afim de disponibilizar APIs REST que provenham as seguintes informações:

1. Dentre os usuários dos tweets buscados, os 5 (cinco) que possuem mais seguidores; :white_check_mark:
2. O total de postagens, agrupadas por hora do dia (independentemente da hashtag); :white_check_mark:
3. O total de postagens para cada uma das hashtags por idioma/país do usuário que postou :x:

Para inicialização rapida do projeto, executar o [quick-start](#quick-start)
<br>

-----

A stack consiste das seguintes tecnologias:

- Linguagem: [Python 3](https://www.python.org/)
- Lib API Twitter: [Tweepy](https://www.tweepy.org/)
- Framework APIs: [Flask](https://palletsprojects.com/p/flask/)
- Monitoramento: [Prometheus](https://prometheus.io/)
- Logs: 
    - [Elasticsearch](https://www.elastic.co/pt/elasticsearch/) 
    - [Filebeat](https://www.elastic.co/pt/beats/filebeat)
    - [Kibana](https://www.elastic.co/pt/kibana)
<br>


-----
## <a name=quick-start></a>Quick Start
<br>

#### Requisitos:

- [Docker](https://www.docker.com/products/docker-desktop) 20.10.2+
- [Docker Compose](https://docs.docker.com/compose/install/) 1.27.4+

Caso queira executar os scripts Python localmente:

- [Python](https://www.python.org/) 3.6.12+
- [PyPi (pip)](https://pypi.org/project/pip/) 21.0.1+
- Demais requisitos no arquivo [requirements.txt](twitter_api/requirements.txt)
<br>

#### Setup:
<br>

##### :warning: Caso `git rev-parse --show-toplevel` não seja um comando valido para o seu sistema operacional, considere nos comandos abaixo o diretório raiz deste projeto git.
<br>

##### 1. Definir as variáveis de ambiente necessárias.

Exportar as credenciais para suas respectivas variáveis (substitua os comandos abaixo com suas chaves)

```
export CONSUMER_KEY=<your-consumer-key>
export CONSUMER_SECRET=<your-consumer-secret>
export ACCESS_TOKEN=<your-access-token>
export ACCESS_TOKEN_SECRET=<your-access-token-secret>
```
<br>

Para execução local dos scripts python, exportar também as seguintes variáveis, com as informações de acesso ao mongodb:

```
export MONGO_SERVER='mongodb://mongo:27017'
export MONGO_USER=root
export MONGO_PWD=mypass
```
<br>

##### 2. (Opcional) Realizar o build da imagem docker.
<br>


OBS: A imagem está versionada repositorio `ocontini/twitter_api` no [dockerhub](https://hub.docker.com)

```
cd `git rev-parse --show-toplevel`/twitter_api && docker build -f ../deploy/Dockerfile -t ocontini/twitter_api .
```

##### 3. Realizar o start da stack.

```
docker-compose -f `git rev-parse --show-toplevel`/deploy/docker-compose.yml up -d
```

- Neste momento, os serviços serão inicializados e em alguns segundos as APIs estarão prontas para receber acessos. Para instruções, ver [Acessando via Postman](#access-apis)
<br>

##### 4. Criar os indices do Kibana no elastic search

```
sh `git rev-parse --show-toplevel`/log-stack/create_index.sh
```
<br>

##### 5. Para realizar o stop da stack

```
docker-compose -f `git rev-parse --show-toplevel`/deploy/docker-compose.yml down
```
<br>

-----

## <a name=about-apis></a>Sobre as APIs
<br>

##### 1. Informações das APIs

Todas as rotas são acessadas pela URL local http://localhost:8081

|        **rotas**       	| **metodos** 	| **ResponseCode:<br>"Success"** 	| **ResponseCode:<br>"Failure"** 	|                                      **descricao**                                      	|
|:----------------------:	|:-----------:	|:------------------------------:	|:------------------------------:	|:---------------------------------------------------------------------------------------:	|
| /api/tweets            	|    `GET`    	|              `200`             	|              `500`             	| Retorna a lista completa dos tweets carregados pelo loader, e salvos no banco de dados. 	|
| /api/rank-by-followers 	|    `GET`    	|              `200`             	|              `500`             	| Retorna o top 5 usuarios com mais seguidores, dentre os tweets coletados.               	|
| /api/tweets-per-hour   	|    `GET`    	|              `200`             	|              `500`             	| Retorna o total de tweets por hora do dia, dentre os tweets coletados.                  	|
| /api/reload-tweets     	|    `POST`   	|              `201`             	|              `503`             	| Carrega uma lista atualizada dos tweets e os salva no banco de dados.                   	|
| /metrics               	|    `GET`    	|              `200`             	|              `404`             	| Retorna metricas de uso das APIs, exportadas pela lib [prometheus-flask-exporter](https://pypi.org/project/prometheus-flask-exporter/)       	|

<br>
##### 2. <a name=access-apis></a>Acessando via Postman

Importar a collection Twitter-Search-API.postman_colection.json, contida na raiz deste repositorio.

OBS: para instruções de como importar uma collection, ver esta [Documentação](https://learning.postman.com/docs/getting-started/importing-and-exporting-data/#importing-data-into-postman).

-----

## <a name=about-apis></a>Monitoramento
<br>

##### Dashboard Grafana

![Dashboard Grafana](https://user-images.githubusercontent.com/15928493/107487972-84464a00-6b65-11eb-9412-f2ba866b30f0.png)
<br>

## <a name=about-apis></a>Logs
<br>

##### View Kibana

![Kibana View](https://user-images.githubusercontent.com/15928493/107518496-d4390700-6b8d-11eb-8eb3-68271f5afb72.png)
