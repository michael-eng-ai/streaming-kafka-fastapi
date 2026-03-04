import json
import redis
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Real-Time Market Data API",
    description="High-performance API fetching real-time financial data computed from a Kafka Steam into Redis.",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis Connection Pooling for fast endpoint responses
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.get("/")
def root():
    return {"message": "Bem vindo a API de Streaming em Tempo Real! Acesse /docs para o Swagger."}

@app.get("/api/v1/ticker/{symbol}")
def get_latest_ticker(symbol: str):
    """
    Recupera em O(1) o último preço transacionado da moeda lendo direto da Hash no Redis.
    """
    symbol = symbol.upper()
    data = redis_client.hgetall(f"ticker:{symbol}")
    
    if not data:
        raise HTTPException(status_code=404, detail="Ticker não encontrado ou dados ainda não recebidos pelo Kafka.")
    
    # Casting back to types
    return {
        "symbol": symbol,
        "price": float(data.get("price", 0)),
        "timestamp": int(data.get("timestamp", 0))
    }

@app.get("/api/v1/history/{symbol}")
def get_ticker_history(symbol: str):
    """
    Recupera os últimos 60 preços históricos da ação transacionados no stream do Kafka via Redis Sorted Sets.
    """
    symbol = symbol.upper()
    history_key = f"history:{symbol}"
    
    # Pega os ultimos 60 registros cronologicamente
    results = redis_client.zrange(history_key, 0, -1)
    
    if not results:
        raise HTTPException(status_code=404, detail="Histórico indisponível")
        
    parsed_results = [json.loads(r) for r in results]
    
    return {
        "symbol": symbol,
        "history": parsed_results
    }
