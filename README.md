
# 🕷️ Async Web Crawling System — FastAPI + RabbitMQ + Workers

Sistema assíncrono de coleta de dados com scraping distribuído, filas de mensagens, processamento em background e API REST.

Este projeto implementa um pipeline completo de data collection com arquitetura baseada em jobs.

---

# 🚀 Visão Geral

A aplicação permite:

- Coletar dados de múltiplas fontes web
- Gerenciar jobs assíncronos via RabbitMQ
- Processar scraping em workers distribuídos
- Persistir resultados em PostgreSQL
- Consultar status e resultados via API REST
- Executar testes automatizados com Testcontainers
- Executar ambiente completo via Docker Compose
- Rodar pipeline CI com GitHub Actions

---

# 🧠 Arquitetura

```

Client → FastAPI → RabbitMQ → Worker → PostgreSQL

```

## Fluxo

1. API agenda job (`POST /crawl/*`)
2. Job é salvo no banco
3. Mensagem é publicada no RabbitMQ
4. Worker consome mensagem
5. Worker executa scraper
6. Resultados são persistidos
7. Job é atualizado para `completed`

---

# 📦 Stack Tecnológica

- FastAPI — API assíncrona
- SQLAlchemy — ORM
- PostgreSQL — persistência
- RabbitMQ — message queue
- aio-pika — client RabbitMQ async
- httpx — HTTP client async
- BeautifulSoup — parsing HTML
- Docker + Docker Compose — containerização
- pytest — testes
- Testcontainers — integração com DB real
- GitHub Actions — CI

---

# 🧩 Arquitetura do Código

```

app/
├── api/                # rotas FastAPI
├── core/               # configurações
├── domain/
│   ├── models/         # entidades de domínio
│   ├── repositories/   # acesso a dados
│   └── services/       # lógica de negócio
├── infrastructure/
│   ├── db/
│   ├── messaging/      # RabbitMQ
│   └── scrapers/
├── workers/            # processamento background

````

### Separação clara de responsabilidades:

- **domain** → regras de negócio
- **infrastructure** → I/O externo
- **api** → interface HTTP
- **workers** → processamento assíncrono

---

# 🎯 Sites Coletados

## Hockey Teams
- HTML com paginação
- Parsing via BeautifulSoup

Dados:
- team_name
- year
- wins/losses
- win_pct
- goals_for / against

## Oscar Films
- Endpoint AJAX
- Parsing JSON

Dados:
- year
- title
- nominations
- awards
- best_picture

---

# ⚙️ Como Rodar

## Requisitos
- Docker
- Docker Compose

## Subir ambiente completo

```bash
docker compose up --build
````

Serviços iniciados:

* API → [http://localhost:8000](http://localhost:8000)
* RabbitMQ UI → [http://localhost:15672](http://localhost:15672)
* PostgreSQL → localhost:5432

---

# 🔌 API Endpoints

## Você pode verificar os endpoints disponíveis em [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI).


# 🧾 Persistência e Auditoria

## Jobs

Cada execução possui:

* type
* error_message
* created_at

Estados:

```
pending → running → completed | failed
```

---

## Job Results (Auditoria)

Foi implementado histórico de execução.

Cada linha registra:

* job_id
* data

Isso permite:

* rastreabilidade
* debugging
* reprocessamento
* observabilidade

---

# 🧪 Testes

## Rodar testes

```bash
pytest -v
```

### Cobertura:

* API endpoints
* criação de jobs
* status de jobs
* persistência
* integração com PostgreSQL real via Testcontainers
* mocking do RabbitMQ publish

Testes não executam scraping real (boa prática).

---

# 🐳 Docker

Ambiente completo:

* API container
* Worker container
* PostgreSQL
* RabbitMQ

Worker roda independente da API.

---

# 🔄 CI com GitHub Actions

Pipeline executa:

* instalação dependências
* lint
* testes unitários
* testes de integração
* build Docker image

## Sobre push para Google Container Registry

O push para GCR não foi incluído por dois motivos:

* requer credenciais específicas do projeto
* não é possível publicar imagens externas em ambiente de avaliação

A configuração é trivial (auth + docker push) e pode ser adicionada facilmente.

---

# 🧱 Decisões Arquiteturais

## Jobs desacoplados dos dados

Dados coletados não possuem relação direta com Job.

Motivos:

* evitar duplicação massiva
* permitir reprocessamento
* manter histórico de execução separado
* melhorar performance

Auditoria é feita via `job_results`.

---

## Bulk insert

Uso de `bulk_insert_mappings` para:

* performance
* baixo overhead ORM
* melhor throughput

---

## Worker isolado

Worker roda como processo independente:

* horizontal scaling
* resiliente a falhas da API
* processamento paralelo

---

## Retry e timeout nos scrapers

Implementado:

* retry
* timeout HTTP
* parsing resiliente
* fallback seguro

---

# 🔮 Melhorias Futuras (Roadmap Arquitetural)

## Observabilidade

* structured logging (JSON logs)
* OpenTelemetry tracing
* metrics com Prometheus
* dashboard Grafana

## Robustez

* retry com backoff no worker
* dead letter queue
* idempotência de jobs
* deduplicação de dados

## Performance

* batch processing configurável
* streaming insert
* cache de scraping

## Escalabilidade

* autoscaling de workers
* partição de filas
* Kubernetes deployment

## API

* paginação de resultados
* filtros
* rate limiting
* autenticação

## Infraestrutura

* deploy em Kubernetes
* Terraform provisioning
* CI/CD com deploy automático

## Scraping

* suporte a Selenium
* detecção de bloqueios
* rotating proxies

---

# 👨‍💻 Autor

Matheus Kolln
