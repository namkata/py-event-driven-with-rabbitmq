from dotenv import load_dotenv
import pika
import os

# Load environment variables from .env file
load_dotenv()

# Get RabbitMQ server information from environment variables
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME", None)
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", None)
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", None)

# Exchange configuration from environment variables
RABBITMQ_EXCHANGE_NAME = os.getenv("RABBITMQ_EXCHANGE_NAME")
RABBITMQ_EXCHANGE_TYPE = os.getenv("RABBITMQ_EXCHANGE_TYPE")
RABBITMQ_ROUTING_KEY = os.getenv("RABBITMQ_ROUTING_KEY")
RABBITMQ_QUEUE_NAME = os.getenv("RABBITMQ_QUEUE_NAME")


def get_rabbitmq_connection():
    """
    Establishes a connection with RabbitMQ server using provided or optional credentials and vhost.

    :return: Connection object to RabbitMQ server
    :rtype: pika.BlockingConnection
    """
    try:
        # Check for presence of credentials and vhost
        credentials = None
        if RABBITMQ_USERNAME and RABBITMQ_PASSWORD:
            credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)

        vhost = RABBITMQ_VHOST
        # Establish connection with RabbitMQ server
        parameters = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            virtual_host=vhost,
            credentials=credentials,
        )
        return pika.BlockingConnection(parameters)
    except Exception as e:
        print(f"Failed to establish RabbitMQ connection: {e}")
        return None


# Vietnamese (vi) docstring
get_rabbitmq_connection.__doc__ = """
    Thiết lập kết nối với máy chủ RabbitMQ sử dụng thông tin về tài khoản và vhost được cung cấp hoặc tùy chọn.

    :return: Đối tượng Kết nối tới máy chủ RabbitMQ
    :rtype: pika.BlockingConnection
    """

# English (en) docstring
get_rabbitmq_connection.__doc__ = """
    Establishes a connection with RabbitMQ server using provided or optional credentials and vhost.

    :return: Connection object to RabbitMQ server
    :rtype: pika.BlockingConnection
    """


def configure_exchange():
    # Setting up the exchange
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()

        channel.exchange_declare(
            exchange=RABBITMQ_EXCHANGE_NAME, exchange_type=RABBITMQ_EXCHANGE_TYPE
        )

        print(f"Exchange '{RABBITMQ_EXCHANGE_NAME}' configured successfully.")
        connection.close()
    except Exception as e:
        print(f"Failed to configure exchange: {e}")


def configure_queue():
    # Configuring the queue
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()

        channel.queue_declare(queue=RABBITMQ_QUEUE_NAME)

        channel.queue_bind(
            exchange=RABBITMQ_EXCHANGE_NAME,
            queue=RABBITMQ_QUEUE_NAME,
            routing_key=RABBITMQ_ROUTING_KEY,
        )

        print(f"Queue '{RABBITMQ_QUEUE_NAME}' configured successfully.")
        connection.close()
    except Exception as e:
        print(f"Failed to configure queue: {e}")
