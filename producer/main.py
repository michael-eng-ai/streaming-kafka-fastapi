import sys
import json
import time
import random
import logging
from typing import List, Dict, Any, Optional
from confluent_kafka import Producer

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'market-ticks'

# Initialize Producer
conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'client.id': 'python-producer'
}

producer = Producer(conf)

def delivery_report(err: Optional[str], msg: Any) -> None:
    """ Called once for each message produced to indicate delivery result. """
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def fetch_market_data() -> List[Dict[str, Any]]:
    """ 
    Simulates extracting real-time ticker string data from a financial API 
    (e.g., Binance WebSockets or Yahoo Finance API).
    """
    tickers = ['AAPL', 'GOOGL', 'AMZN', 'TSLA', 'BTC-USD', 'ETH-USD']
    data = []
    
    for _ in range(3): # Gera 3 ticks aleatórios por ciclo
        ticker = random.choice(tickers)
        base_price = 100.0 if 'USD' not in ticker else 50000.0
        # Simula flutuação de preço entre -1% a +1%
        fluctuation = random.uniform(-0.01, 0.01)
        price = base_price * (1 + fluctuation)
        
        tick = {
            "symbol": ticker,
            "price": round(price, 2),
            "timestamp": int(time.time() * 1000) # milissegundos
        }
        data.append(tick)
    
    return data

def run_producer() -> None:
    logger.info(f"Starting Kafka Producer on {KAFKA_BROKER}")
    logger.info(f"Publishing to topic: {TOPIC_NAME}")
    logger.info("Press Ctrl+C to exit...")
    
    try:
        while True:
            # Puxa os "dados em tempo real"
            ticks = fetch_market_data()
            
            for tick in ticks:
                # Serializa o dict para JSON byte string
                payload = json.dumps(tick).encode('utf-8')
                
                # Produz a mensagem assincronamente (Fire and Forget)
                producer.produce(
                    topic=TOPIC_NAME, 
                    value=payload, 
                    key=tick['symbol'].encode('utf-8'), # A key garante que updates da mesma moeda vão pra mesma partição
                    callback=delivery_report
                )
            
            # Chama eventos de callback (delivery reports) enfileirados
            producer.poll(0)
            
            # Espera 1 segundo para a próxima "Buscada na API"
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Stopping Producer...")
    except Exception as e:
        logger.exception("An unexpected error occurred in the producer loop.")
        raise
    finally:
        # Espera mensagens flutuantes serem escoadas antes de desligar
        logger.info("Flushing remaining messages...")
        producer.flush(timeout=5.0)

if __name__ == '__main__':
    run_producer()
