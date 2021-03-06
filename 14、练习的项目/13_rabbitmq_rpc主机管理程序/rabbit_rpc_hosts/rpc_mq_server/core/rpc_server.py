# _*_coding:utf-8_*_
from conf.settings import MQ_QUEUE_NAME
from core.handler import run_cmd
import pika
import json
import logging

logger = logging.getLogger("rabbit_mq.task")


class RpcServer(object):
    def __init__(self, host, port, virtual_host, username, password):
        # 声明mq连接用户、连接实例、声明使用管道、声明使用的队列名称
        credentials = pika.PlainCredentials(username, password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,
                                                                       port=port,
                                                                       virtual_host=virtual_host,
                                                                       credentials=credentials))
        self.channel = connection.channel()
        self.channel.queue_declare(queue=MQ_QUEUE_NAME, durable=True)  # durable=True队列持久化
        self.channel.basic_consume(self.get_response, queue=MQ_QUEUE_NAME)

    @staticmethod
    def handler(task_id, commands):
        """
        :param task_id: 任务id
        :param commands: 请求数据，1个或多个可执行的命令，以逗号连接
        :return: 请求返回结果，命令的执行结果
        """
        commands = commands.decode(encoding="utf-8")
        logger.debug("开始执行命令{0}".format(commands))
        rsp = run_cmd(task_id, commands)
        logger.debug("执行命令{0}结束，结果：{1}".format(commands, rsp.__dict__))
        return json.dumps(rsp.__dict__)

    def get_response(self, ch, method, props, body):
        """
        :param ch: 队列管道channel对象
        :param method:请求方法对象
        :param props:请求属性对象
        :param body:请求数据
        :return: 请求处理结果
        """
        # 客户端发送的请求task_id
        task_id = props.correlation_id
        # 处理请求
        response = self.handler(task_id, body)
        # 请求返回数据通过客户端指定的队列（reply_to）返回给客户端
        response_queue = props.reply_to

        # 执行推送消息，delivery_mode=2消息持久化
        ch.basic_publish(exchange='',
                         routing_key=response_queue,
                         properties=pika.BasicProperties(correlation_id=task_id, delivery_mode=2),
                         body=response)
        # 如果发送端设置了需ack验证，则处理完消息后，要发送确认信息。否则，不会移除队列中的该条消息
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        self.channel.start_consuming()
