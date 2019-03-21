# RabbitMq with MQTT

1. `pip install DockerBuildManagement`
2. Build: `dbm -build`
3. Run in swarm: `dbm -swarm -start`
4. Login to rabbitmq management ui (amqp/amqp): https://localhost:15672
5. Stop services: `dbm -swarm -stop`

## Buildsystem:
- [DockerBuildManagement](https://github.com/DIPSAS/DockerBuildManagement/blob/master/README.md)