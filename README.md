# Real-Time Streaming Radar

![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-000?style=for-the-badge&logo=apachekafka) ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

Este projeto implementa e documenta uma arquitetura de dados corporativa estritamente orientada a eventos (Event-Driven Architecture) padronizada para contextos reais envolvendo alta volumetria distribuída (Real-Time Streaming). A integralidade tecnológica presente no ecossistema comporta-se de forma estritamente modular, mantida integralmente conteinerizada por meio do padrão de orquestração Docker.

## Modelagem dos Microsserviços

O pipeline encontra-se devidamente segmentado e distribuído em 6 sub-sistemas independentes e comunicantes entre a sub-rede estrita e padronizada (`streaming-net`):

1. **Broker Principal (`kafka` & `zookeeper`)**: O núcleo resiliente de distribuição pautado nas imagens consolidadas pela entidade provedora Confluent, coordenando de forma redundante e estrita as matrizes assíncronas de fluxos mantidas de forma lógica em tópicos.
2. **Python Producer (`python-producer`)**: Interface de injeção ponta a ponta configurada autonomamente, produzindo carga analítica e financeira de mercado. Emitindo ocorrências estritas a título de cotação temporal em fluxo persistente voltado para a instância transacional configurada (`market-ticks`).
3. **Python Consumer (`python-consumer`)**: Aplicação distribuída orientada de forma estrita para tratamento e extração in-stream assíncrona base. Transaciona os binários capturados em interface conectada com instâncias de banco temporal operante (cálculo vetorial da aplicação).
4. **Sessões e Memória de Serving (`redis`)**: Opera nativamente compondo a estrutura matricial da *Speed Layer* fundamentada globalmente na infraestrutura formal de arquiteturas lógicas tipo Lambda/Kappa. Garante que os registros primários de cálculo da camada anterior contem com estabilização temporal e cálculo algorítmico em nível ótimo transacional (`O(1)`).
5. **Aplicação Final API (`fastapi-app`)**: Interface construída provendo e assegurando integração RESTful a camada assíncrona orientada via requisição global sobre os nós provisionados. Proporciona atendimento a requisições com latência aferida em índices compatíveis e escaláveis.
6. **Interface de Observabilidade (`kafka-ui`)**: Monitor visual contido, utilizado amplamente no dimensionamento infraestrutural do gerenciamento ativo sobre tópicos, brokers atrelados e partições estruturadas.

---

## Deployment Local Integrado (Containerização)

A arquitetura encontra-se plenamente aliviada de dependências sistemáticas colaterais, fundamentando seu fluxo operacional de setup no utilitário de mercado Docker.

```bash
# Implantação e Transição Sistemática Inicial
git clone https://github.com/michael-eng-ai/streaming-kafka-fastapi.git
cd streaming-kafka-fastapi

# Renderização Base do Workflow Integrado
docker compose up --build -d
```

### Observabilidade Base

Em seções transacionais, os subprodutos comportamentais emitidos através dos Microsserviços Python acoplados devem ser monitorados pelas bibliotecas integradas na esteira dos Containers do Pipeline:
```bash
# Fluxo de Inspeção Produtora a nível Kernel
docker logs python-producer -f

# Fluxo de Inspeção Processual Analítica a nível Kernel
docker logs python-consumer -f
```

## Integregação Pública Externa (REST Endpoints)

A API provê integração estrutural pautada via Swagger (compatível com os frameworks estritos da especificação padrão do OpenAPI). 

Acesse os direcionamentos listados sob a host sub-provida local:

- **Documentação Formal Sistêmica (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Aferição Estrutural Temporal:** `GET http://localhost:8000/api/v1/ticker/{symbol}` (Especificação Simbólica Ex: `BTC-USD`, `AAPL`, `TSLA`).
- **Recuperação Categórica de Amostragem Janelada:** `GET http://localhost:8000/api/v1/history/{symbol}`.

### Utilitário Concorrente (Cluster Kafka Management)
- **Kafka UI Manager Interface:** [http://localhost:8080/](http://localhost:8080/) (Interface Web).

---

## Encerramento da Arquitetura Analítica Local

Para desassociação governada das redes e processos temporais isolados:
```bash
docker compose down --volumes
```

> *Construção modelada formalmente à comprovação em padrões analíticos industriais com garantia global aplicável, modularidade de Microsserviços e resiliência governada de falha por desacoplamento comunicativo.*
