FROM arm64v8/rabbitmq:3.11.5-management

RUN rabbitmq-plugins enable rabbitmq_mqtt
RUN rabbitmq-plugins enable rabbitmq_web_mqtt

ADD rabbitmq.conf /etc/rabbitmq/