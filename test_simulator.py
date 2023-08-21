import os
import threading
from time import sleep

import pika
import requests
from flask import Flask, request

app = Flask(__name__)
adresa_simluacionog_servisa = os.environ.get("adresa_simluacionog_servisa", "http://localhost:5002")
sleep(30)
# connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
# channel = connection.channel()


@app.route('/ucitaj_blokove', methods=['POST'])
def ucitaj_blokove():
    print('stigao zahtjev')
    data = request.json
    result = requests.post(url=f'{adresa_simluacionog_servisa}/ucitaj', json=data)
    return result.text


@app.route('/obradi_niz_blokova', methods=['POST'])
def obradi_niz_blokova():
    data = request.json
    result = requests.post(url=f'{adresa_simluacionog_servisa}/obradi', json=data)
    return result.text


@app.route('/sortiraj_niz', methods=['POST'])
def sortiraj_niz():
    data = request.json
    result = requests.post(url=f'{adresa_simluacionog_servisa}/sortiraj', json=data)
    return result.text



@app.route('/pokreni_simulaciju', methods=['POST'])
def pokreni_simulaciju():
    data = request.json
    result = requests.post(url=f'{adresa_simluacionog_servisa}/pokreni', json=data)
    return result.text


@app.route('/pauziraj_simulaciju/<nit>', methods=['GET'])
def pauziraj_simulaciju(nit):
    result = requests.get(url=f'{adresa_simluacionog_servisa}/pauziraj/{nit}')
    return result.text


@app.route('/nastavi_simulaciju/<nit>', methods=['GET'])
def nastavi_simulaciju(nit):
    result = requests.get(url=f'{adresa_simluacionog_servisa}/nastavi/{nit}')
    return result.text

class PikaMassenger():

    exchange_name = '...'

    def __init__(self, *args, **kwargs):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        self.channel = self.conn.channel()

    def consume(self, keys, callback):
        self.channel.queue_declare('gotove_simulacije')

        self.channel.basic_consume(
            queue='gotove_simulacije',
            on_message_callback=callback,
            auto_ack=True)

        self.channel.start_consuming()


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

def start_consumer():

    def callback(ch, method, properties, body):
        print(" [x] %r:%r Procitao" % (method.routing_key, body))

    with PikaMassenger() as consumer:
        consumer.consume(keys=[...], callback=callback)

if __name__ == "__main__":
    # channel.queue_declare(queue='gotove_simulacije')
    # channel.basic_consume(queue='gotove_simulacije', auto_ack=True, on_message_callback=callback)
    # print(' [*] Cekam poruke. To exit press CTRL+C')
    # channel.start_consuming()
    consumer_thread = threading.Thread(target=start_consumer)
    consumer_thread.start()
    app.run(host='0.0.0.0')

