# ✈️ Travel Planner - API (Back-End)

Este repositório contém o módulo de serviços e banco de dados (Back-End) para a aplicação **Travel Planner**, desenvolvida como MVP para a disciplina de Arquitetura de Software.

A aplicação disponibiliza uma API RESTful desenvolvida em Python (Flask) para o gerenciamento de roteiros de viagens (com operações de CRUD completo) e integração com serviços externos para consulta de informações sobre destinos turísticos e cidades.

---

## 🏗️ Arquitetura da Solução

O projeto segue o **Cenário 1** das diretrizes da disciplina, no qual esta API Back-End em Python (Flask) é responsável pela persistência de dados em banco SQLite (via SQLAlchemy), além de intermediar a comunicação com uma API pública externa (atuando como proxy) para consulta de dados geográficos e demográficos de destinos.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+** como linguagem principal
- **Flask & flask-openapi3** para criação da API RESTful e documentação Swagger
- **Flask-CORS** para controle e liberação de requisições do Front-End
- **SQLAlchemy & SQLite** para mapeamento objeto-relacional (ORM) e persistência de dados
- **Pydantic** para validação e estruturação dos dados dos schemas
- **Requests** para consumo da API externa pública
- **Docker & Docker Compose** para containerização e orquestração do ambiente

---

## 🌐 Consumo das Rotas e APIs

### 1. API Back-End Principal (Endpoints REST)

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/` | Redireciona automaticamente para a documentação interativa Swagger. |
| `GET` | `/viagens` | Lista todas as viagens cadastradas no banco de dados. |
| `POST` | `/viagem` | Cadastra um novo planejamento de viagem (destino, datas, orçamento e bagagem). |
| `PUT` | `/viagem/{id}` | Atualiza os dados de uma viagem cadastrada existente pelo seu ID. |
| `DELETE`| `/viagem/{id}` | Remove uma viagem cadastrada pelo seu ID. |
| `GET` | `/voos/{codigo_iata}` | Consulta informações reais de localização, região e população do destino via API Externa. |

### 2. API Externa Pública Consumida

- **Serviço Consumido:** Open-Meteo Geocoding API (`https://geocoding-api.open-meteo.com/v1/search`)
- **Objetivo:** Consultar dinamicamente o nome oficial da cidade, país, região/estado e população a partir do termo de pesquisa informado (ex: `São Paulo`, `Paris`, `Miami`, `Tokyo`).
- **Licença / Autenticação:** Gratuita e pública (não exige *API Key* ou cadastro).
- **Tratamento de Dados:** A requisição é efetuada pelo Back-End em Flask e enviada em formato JSON ao Front-End. Erros de rede ou termos não encontrados são tratados com códigos de status HTTP reais (`404` e `502`), garantindo o envio exclusivo de informações autênticas.
