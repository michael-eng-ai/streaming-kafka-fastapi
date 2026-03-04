# ⚡ Real-Time Streaming Radar

![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-000?style=for-the-badge&logo=apachekafka) ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

Este projeto demonstra a construção corporativa de uma arquitetura de dados orientada a eventos (*Event-Driven*) para ambientes de alta vazão (Real-Time Streaming). Todo o ecossistema é agnóstico à nuvem e encapsulado via microsserviços do **Docker**.

## 🏗️ Arquitetura dos Microsserviços

O pipeline é comporto por 6 containers rodando em uma rede selada (`streaming-net`):

1. **Broker Principal (`kafka` & `zookeeper`)**: O coração da mensageria (usando as imagens oficiais da Confluent). Mantém os tópicos vivos e garante a resiliência dos pacotes não consumidos.
2. **Python Producer (`python-producer`)**: Um script autônomo que simula um websocket/crawling financeiro. Ele emite "ticks" aleatórios de preço do mercado de ações a cada 1 segundo diretamente em um tópico (`market-ticks`).
3. **Python Consumer (`python-consumer`)**: Um *Worker* que processa a fila infinita do Kafka e age como intermediário (ETL in-stream). Ele pega o binário do Kafka e faz um Upsert veloz em chaves de estado de um banco em-memória.
4. **Fast Storage (`redis`)**: Atua como a camada de *Serving* (Layer de Velocidade / Arquitetura Lambda). O Redis mantem o *State* transacional mais recente (`ticker:AAPL`) calculável em `O(1)`.
5. **API Client (`fastapi-app`)**: Uma API RESTful moderna baseada no padrão ASGI que consulta o cluster do Redis respondendo aos consumidores finais Web em baixíssima latência (milissegundos), poupando o banco de dados analítico de pancadas.
6. **Interface de Observabilidade (`kafka-ui`)**: Um painel Web gráfico provido pela Provectus para monitorar a saúde do broker e inspecionar mensagens trafegando ao vivo.

---

## 🚀 Como Subir o Projeto (One-Click Deploy)

Você **não precisa intalar nada** além do Docker na sua máquina. O Dockerfile dos microsserviços vai abstrair as bibliotecas do Python.

```bash
# Baixe o repositório
git clone https://github.com/michael-eng-ai/streaming-kafka-fastapi.git
cd streaming-kafka-fastapi

# Construa as imagens Python e suba os 6 containers atrelados na rede
docker compose up --build -d
```

### 🔍 Monitorando o Sistema

Acompanhe os logs dos serviços Python para ver a produção e consumo de ponta a ponta ocorrendo:
```bash
# Ver os ticks sendo criados pelo producer a cada segundo
docker logs python-producer -f

# Ver os ticks sendo salvos massivamente no Redis pelo consumer
docker logs python-consumer -f
```

## 🌐 Endpoints Disponíveis (Como Consumir a API)

A FastAPI expõe a documentação auto-gerada do *Swagger* (OpenAPI). 
Com o cluster no ar, acesse no seu navegador local:

- 📖 **Documentação Oficial (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
- 📈 **Recuperar o Preço em Tempo Real:** `GET http://localhost:8000/api/v1/ticker/{symbol}` (Ex: `BTC-USD`, `AAPL`, `TSLA`).
- 🕰️ **Recuperar Histórico de Janela Redes:** `GET http://localhost:8000/api/v1/history/{symbol}`.

### Painel do Cluster Kafka
- 🎛️ **Kafka UI Manger:** [http://localhost:8080/](http://localhost:8080/) (Interface de gestão de brokers/tópicos).

---

## 🧹 Encerrando o Cluster

```bash
docker compose down --volumes
```

> *Desenvolvido para evidenciar a governança sobre tópicos/streaming, a separação modular de responsabilidades em Workers escaláveis e entrega via modelo de Arquitetura de Microsserviços.*
