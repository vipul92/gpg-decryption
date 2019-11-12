from flask import Flask
from flask_restful import Api

from apis import decryption_task
import settings

BASE_HOST = getattr(settings, "BASE_HOST", "0.0.0.0")
BASE_PORT = getattr(settings, "BASE_PORT", "8000")

application = Flask(__name__)
api = Api(application)

api.add_resource(decryption_task.Decrypt, '/decryptMessage')

if __name__ == '__main__':
    application.run(host=BASE_HOST, port=BASE_PORT, debug=True)
