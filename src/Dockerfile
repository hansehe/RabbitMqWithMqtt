FROM rabbitmq:3.9.5-management

RUN rabbitmq-plugins enable rabbitmq_mqtt
RUN rabbitmq-plugins enable rabbitmq_web_mqtt

ADD rabbitmq.conf /etc/rabbitmq/