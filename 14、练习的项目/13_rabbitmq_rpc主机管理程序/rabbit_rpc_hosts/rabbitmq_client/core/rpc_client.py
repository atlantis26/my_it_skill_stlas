# coding:utf-8
from conf.settings import MQ_QUEUE_DICT, CLIENT_QUEUE
from core.db_handler import save_task, load_task
import pika
import uuid


class RpcClient(object):
    def __init__(self, host, port, virtual_host, username, password):
        self.host = host
        self.port = port
        self.virtual_host = virtual_host
        self.username = username
        self.password = password

        # 声明rabbitMq会话session连接、管道channel
        credentials = pika.PlainCredentials(self.username, self.password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host,
                                                                            port=self.port,
                                                                            virtual_host=self.virtual_host,
                                                                            credentials=credentials))
        self.channel = self.connection.channel()
        # 生成一个排它随机队列（amq.*）用于返回请求结果, 排它随机队列在创建它的会话连接connection关闭时自动删除
        # self.random_queue = self.channel.queue_declare(exclusive=True)
        # 更改为使用持久化队列，确保任务的执行结果不会丢失
        self.channel.queue_declare(queue=CLIENT_QUEUE, durable=True)
        self.channel.basic_consume(self.callback, queue=CLIENT_QUEUE)

    def request(self, cmd_args, host):
        """
        不同的server_queue代表不同的rpc_server,即可以根据不同server_queue到不同的服务器上执行命令
        """
        # 声明服务端的队列
        server_queue = MQ_QUEUE_DICT[host]
        self.channel.queue_declare(queue=server_queue, durable=True)
        # 生成执行的任务id
        task_id = str(uuid.uuid4())
        properties = pika.BasicProperties(reply_to=CLIENT_QUEUE,
                                          delivery_mode=2,
                                          correlation_id=task_id)
        self.channel.basic_publish(exchange='',
                                   routing_key=server_queue,
                                   properties=properties,
                                   body=cmd_args)
        # 客户端本地记录下TASK相关信息
        save_task(task_id, CLIENT_QUEUE, None)
        # self.connection.process_data_events()

        return task_id

    def callback(self, ch, method, props, body):
        """
        用于接收任务执行的返回数据，并按照task_id写入到数据库（文件）
        """
        task_id = props.correlation_id
        queue = props.reply_to
        data = body.decode(encoding="utf-8")
        save_task(task_id, queue, data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def response(self, task_id):
        """
        用于执行返回任务执行结果的任务，不新生成队列，而是使用之前创建任务时，生成的随机队列
        """
        # 随机排它队列，不能手动声明，即不能声明名称为“amq.*”的队列，已存在的队列直接使用就可以了
        # self.channel.queue_declare(queue=random_queue)
        data = load_task(task_id)["data"]
        if data is None:
            # 非阻塞发送请求,如果有请求返回结果，则在callback函数中，将返回结果，写入到数据库文件
            self.connection.process_data_events()
            data = load_task(task_id)["data"]
        return data
