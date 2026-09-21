# ✈️ Travel Planner - API (Back-End)

Este repositório contém o módulo de serviços e banco de dados (Back-End) para a aplicação **Travel Planner**, desenvolvida como MVP para a disciplina de Arquitetura de Software.

A aplicação disponibiliza uma API RESTful desenvolvida em Python (Flask) para o gerenciamento de roteiros de viagens (com operações de CRUD completo) e integração com serviços externos para consulta de dados de voos e aeroportos.

---

## 🏗️ Arquitetura da Solução

O projeto segue o **Cenário 1** das diretrizes da disciplina, no qual esta API Back-End em Python (Flask) é responsável pela persistência de dados em banco SQLite (via SQLAlchemy), além de intermediar a comunicação com uma API pública externa para consulta de informações aeroportuárias.

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
| `GET` | `/voos/{codigo_iata}` | Consulta informações e status de aeroportos/voos via API Externa. |

### 2. API Externa Pública Consumida

- **Serviço Consumido:** Louami Airport API (`https://api.louami.com/v1/airport/{codigo}`)
- **Objetivo:** Consultar o nome oficial do aeroporto e o status operacional a partir do código IATA informado (ex: `MIA`, `CWB`, `GRU`), retornando os dados tratados em formato JSON para a interface.

---

├── requirements.txt              # Dependências e bibliotecas do projeto Python
└── README.md                     # Documentação completa da API (Back-End)
