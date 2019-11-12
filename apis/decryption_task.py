import os
import gnupg
from pathlib import Path

from flask import request
from flask_restful import Resource

import settings

BASE_DIR = getattr(settings, "BASE_DIR", "")
GPG_HOME = getattr(settings, "GPG_HOME", "")
KEY = getattr(settings, "KEY", "")

ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL", "vipul.kumar@valuecoders.com")

gpg = gnupg.GPG(gnupghome=GPG_HOME)


class Decrypt(Resource):
    """
    Decrypts the message from request

    :method: POST
    :accept-encoding: 'application/json'
    :params: 'passphrase' and 'message'

    :response: 
        'decrypted_message', 200 (Success)
        'error_message', 400 (Failure/Error)

    """

    def post(self):
        if not request.is_json:
            return "Bad Request: Expecting Content-Type to be 'application/json'", 400

        data = request.json
        _encrypted_message = data.get("message", None)
        _passphrase = data.get("passphrase", None)
        if _passphrase is None or _encrypted_message is None:
            if _passphrase is None and _encrypted_message is None:
                return "Invalid Request: 'passphrase' and 'message' missing in request", 400
            if _encrypted_message is None:
                return "Invalid Request: 'message' missing in request", 400

            return "Invalid Request: 'passphrase' missing in request", 400
        
        self.remove_keys()
        _key = self.generate_keys(_passphrase)
        self.export_keys(_key, _passphrase)
        self.import_keys()

        decrypted_data = self.decrypt_message(_encrypted_message, _passphrase)
        if decrypted_data.status == "decryption ok":
            response = {"DecryptedMessage":str(decrypted_data)}
            return response, 200

        return "Unknown error in decrypting the message", 400

    def remove_keys(self):
        try:
            os.system('rm {}'.format(KEY))
        except Exception as err:
            print("Keys does not exits")

        return True

    def generate_keys(self, passphrase):
        data = gpg.gen_key_input(
            name_email=ADMIN_EMAIL,
            passphrase=passphrase)
        
        return gpg.gen_key(data)

    def import_keys(self):
        key_data = open(KEY).read()
        import_result = gpg.import_keys(key_data)

        return True

    def export_keys(self, key, passphrase):
        public_keys = gpg.export_keys(
            key.fingerprint, passphrase=passphrase)

        private_keys = gpg.export_keys(
            key.fingerprint, True, passphrase=passphrase)

        with open(KEY, 'w+') as f:
            f.write(public_keys)
            f.write(private_keys)

        return True

    def list_keys(self):
        public_keys = gpg.list_keys()
        private_keys = gpg.list_keys(True)

        return True

    def decrypt_message(self, encrypted_message, passphrase):
        decrypted_data = gpg.decrypt(
            encrypted_message, passphrase=passphrase)

        return decrypted_data