import os
from os import path
import gnupg
import unittest
from apis import decryption_task as dt
import settings

GPG_HOME = getattr(settings, "BASE_DIR", "") + "/gpghome"
KEY = getattr(settings, "KEY", "")

os.system('mkdir -p gpghome')

request_data = {
"message": "-----BEGIN PGP MESSAGE-----\nVersion: GnuPG v2\njA0ECQMCVady3RUyJw3X0kcBF+zdkfZOMhISoYBRwR3uk3vNv+TEg+rJnp4/yYISpEoI2S82c\nDiCNBIVAYWB8WKPtH2R2YSussKhpSJ4mFgqyOA01uwroA===KvJQ\n-----END PGP MESSAGE-----",
"passphrase": "topsecret"
}

decrypt = dt.Decrypt()

gpg = gnupg.GPG(gnupghome=GPG_HOME)


class TestFunctions(unittest.TestCase):

    def test_key_generation(self):
        _key = decrypt.generate_keys(request_data["passphrase"])

        self.assertEquals(type(_key), gnupg.GenKey)

    def test_key_export(self):
        _key = decrypt.generate_keys(request_data["passphrase"])
        ex = decrypt.export_keys(_key, request_data["passphrase"])

        # public_keys = gpg.list_keys()
        # private_keys = gpg.list_keys(True)

        # self.assertNotEquals(len(public_keys), 0)
        # self.assertNotEquals(len(private_keys), 0)

    def test_key_removal(self):
        decrypt.remove_keys()
        _key = path.exists(KEY)

        self.assertFalse(_key)

    # def test_message_decryption(self):
    #     decrypt.remove_keys()
    #     _key = decrypt.generate_keys(request_data["passphrase"])
    #     decrypt.export_keys(_key, request_data["passphrase"])
    #     decrypt.import_keys()
    #     decrypted_data = decrypt.decrypt_message(request_data["message"], request_data["passphrase"])

    #     self.assertEquals(decrypted_data.status, "decryption ok")


if __name__ == '__main__':
      unittest.main()