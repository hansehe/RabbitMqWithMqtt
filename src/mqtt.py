import paho.mqtt.client as mqtt
import uuid
import ssl
import json
from typing import Dict, List

# pip install paho-mqtt

TOPIC = 'myTopic'
QOS = 2 # 0, 1 or 2
# read about qos here: https://www.hivemq.com/blog/mqtt-essentials-part-6-mqtt-quality-of-service-levels/
# and here: https://www.rabbitmq.com/mqtt.html#features

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client: mqtt.Client, userdata: object, flags: Dict[str, int], rc: int):
    global QOS, TOPIC
    print(f'Connected with result code {str(rc)}')

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    result, mid = client.subscribe(TOPIC, qos=QOS)
    assert result == mqtt.MQTT_ERR_SUCCESS

# The callback for when a PUBLISH message is received from the server.
def on_message(client: mqtt.Client, userdata: object, msg: mqtt.MQTTMessage):
    global QOS, TOPIC
    msgString = str(msg.payload.decode('utf-8'))
    print(f'{msg.topic}: {msgString}')


def on_disconnect(client, userdata: object, rc: int):
    print('Disconnected with result code '+str(rc))


def get_client(clientNumber: int = None) -> mqtt.Client:
    if clientNumber is None:
        clientNumber = uuid.uuid1()
    clientId = f'mqtt-test-{clientNumber}'
    client = mqtt.Client(client_id=clientId, clean_session=True, transport='websockets')
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    host = 'localhost'
    port = 15675
    tls = False
    insecureTls = True

    client.ws_set_options(path='/ws', headers=None)
    if tls and insecureTls:
        client.tls_set(cert_reqs=ssl.CERT_NONE)
        client.tls_insecure_set(True)
    elif tls:
        client.tls_set()
    username = 'amqp'
    password = 'amqp'
    virtualhost = '/'
    mqttUsername = username
    if len(virtualhost) > 0:
        mqttUsername = f'{virtualhost}:{mqttUsername}'
    client.username_pw_set(mqttUsername, password=password)
    client.connect(host, port=port, keepalive=3)
    return client


n_clients = 2
clients: List[mqtt.Client] = []
for i in range(n_clients):
    print(f'Creating mqtt client {i+1}')
    clients.append(get_client(i+1))

for client in clients:
    client.loop_start()

infoInput = 'Hit enter with no inputs to stop..'
stringInput = input(infoInput)
while len(stringInput) > 0:
    for client in clients:
        payload = {'msg': f'Hello Mqtt World! From client {str(client._client_id.decode("utf-8"))}'}
        info: mqtt.MQTTMessageInfo = client.publish(TOPIC, json.dumps(payload), qos=QOS, retain=True)
        info.wait_for_publish()
        print(f'published successfully on topic: {TOPIC}')
    stringInput = input(infoInput)

for client in clients:
    print(f'Stopping mqtt client {str(client._client_id.decode("utf-8"))}')
    client.loop_stop(force=True)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()
