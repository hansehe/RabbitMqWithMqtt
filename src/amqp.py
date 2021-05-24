import pika
import logging
from PikaBus.abstractions.AbstractPikaBus import AbstractPikaBus
from PikaBus.abstractions.AbstractPikaBusSetup import AbstractPikaBusSetup
from PikaBus.PikaBusSetup import PikaBusSetup

# pip install pikabus

logging.basicConfig(format=f'[%(levelname)s] %(name)s - %(message)s', level='WARNING')


def MessageHandlerMethod(**kwargs):
    """
    A message handler method may simply be a method with som **kwargs.
    The **kwargs will be given all incoming pipeline data, the bus and the incoming payload.
    """
    data: dict = kwargs['data']
    bus: AbstractPikaBus = kwargs['bus']
    payload: dict = kwargs['payload']
    print(payload)
    if 'count' in payload:
        payload['count'] += 1
        # bus.Publish(payload, topic='myTopic')


host = 'localhost'

credentials = pika.PlainCredentials('amqp', 'amqp')
connParams = pika.ConnectionParameters(
    host=host,
    port=5672,
    virtual_host='/',
    credentials=credentials)

pikaBusSetup: AbstractPikaBusSetup = PikaBusSetup(connParams,
                                                  defaultDirectExchange='amq.direct',
                                                  defaultTopicExchange='amq.topic',
                                                  defaultListenerQueue='myQueue',
                                                  defaultSubscriptions='myTopic')
pikaBusSetup.AddMessageHandler(MessageHandlerMethod)


nQueues = 2
consumingTasks = []
bus: AbstractPikaBus = pikaBusSetup.CreateBus()
for i in range(nQueues):
    listenerQueue = f'myQueue-{i}'
    pikaBusSetup.Init(listenerQueue=listenerQueue)
    consumingTasks += pikaBusSetup.StartConsumers(consumerCount=1,
                                                  listenerQueue=listenerQueue)

    bus.Subscribe('myTopic', queue=listenerQueue)
payload = {'hello': 'amqp!', 'count': 0}

bus.Publish(payload=payload, topic='myTopic')

input('Hit enter to stop all consuming channels \n\n')
pikaBusSetup.StopConsumers()