import sys
import json
import redis
from confluent_kafka import Consumer, KafkaException, KafkaError

# Configurations
KAFKA_BROKER = 'kafka:29092' # internal docker network
TOPIC_NAME = 'market-ticks'
REDIS_HOST = 'redis'
REDIS_PORT = 6379

# Initialize Redis Client
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Initialize Kafka Consumer
conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'redis-ingestion-group',
    'auto.offset.reset': 'latest' # Em streaming financeiro, geralmente só importa os dados mais novos
}

consumer = Consumer(conf)

def run_consumer():
    # Testa conexão com Redis
    try:
        r.ping()
        print(f"✅ Conectado ao Redis em {REDIS_HOST}:{REDIS_PORT}")
    except redis.ConnectionError:
        print("❌ Erro ao conectar no Redis. O serviço está rodando?")
        sys.exit(1)
        
    try:
        consumer.subscribe([TOPIC_NAME])
        print(f"📡 Consumer inscrito no tópico: {TOPIC_NAME}")
        print("👀 Aguardando mensagens do Kafka...\n")

        while True:
            # Bloqueia até chegar uma mensagem (timeout de 1s)
            msg = consumer.poll(timeout=1.0)
            
            if msg is None:
                continue
                
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue # Fim da partição, evento normal
                else:
                    print(f"❌ Erro no Consumer: {msg.error()}")
                    raise KafkaException(msg.error())
            
            # Mensagem recebida com sucesso
            raw_data = msg.value().decode('utf-8')
            tick = json.loads(raw_data)
            
            symbol = tick['symbol']
            price = tick['price']
            timestamp = tick['timestamp']
            
            # ⚡ Armazenamento em Tempo Real no Redis
            # A estratégia aqui é manter o preço mais atual de cada moeda acessível em O(1)
            redis_key = f"ticker:{symbol}"
            
            # Hash in Redis storing price and last_updated
            r.hset(redis_key, mapping={
                "price": price,
                "timestamp": timestamp
            })
            
            # Add to a Timeseries / Sorted Set for historical graph (last 100 prices)
            history_key = f"history:{symbol}"
            r.zadd(history_key, {json.dumps({"p": price, "t": timestamp}): timestamp})
            
            # Cleanup: Mantemos apenas os 60 pontos de dados mais recentes no histórico
            r.zremrangebyrank(history_key, 0, -61)
            
            print(f"💾 Carga Redis --> [{symbol}] U$ {price} armazenado.")

    except KeyboardInterrupt:
        print("\n⏹️ Parando Consumer localmente...")
    finally:
        # Commit de segurança e fechamento graceful connection
        consumer.close()
        print("Done.")

if __name__ == '__main__':
    run_consumer()
