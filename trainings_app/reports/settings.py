import os
import dotenv

dotenv.load_dotenv()

RABBITMQ_CONF = {
    'VHOST': os.getenv('RABBITMQ_DEFAULT_VHOST', '/'),
    'USER': os.getenv('RABBITMQ_DEFAULT_USER', 'guest'),
    'PASS': os.getenv('RABBITMQ_DEFAULT_PASS', 'guest'),
    'HOST': os.getenv('RABBITMQ_HOST', 'localhost'),
}

conf_url = f"pyamqp://{RABBITMQ_CONF['USER']}:{RABBITMQ_CONF['PASS']}@{RABBITMQ_CONF['HOST']}/{RABBITMQ_CONF['VHOST']}"
