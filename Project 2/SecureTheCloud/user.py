from Crypto.PublicKey import RSA
class User:

    def __init__(self, email, credentials, public_key=None, private_key=None):
        self.email = email
        self.credentials = credentials
        self.public_key = public_key
        self.private_key = private_key

        if not self.public_key or not self.private_key:
            self.generate_key_pair()

    def generate_key_pair(self, key_size=2048):
        key = RSA.generate(key_size)
        self.private_key = key.export_key().decode()
        self.public_key = key.publickey().export_key().decode()
