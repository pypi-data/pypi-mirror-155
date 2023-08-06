from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
import base64

# from eClinical import Environment
from eclinical.environment.environment import Environment


class Ecrypto:
    def __init__(self, environment: Environment):
        self.environment = environment

    def en(self, string):
        public_key = self.environment.public_key
        public_key = "-----BEGIN PUBLIC KEY-----\n" + public_key + "\n-----END PUBLIC KEY-----"
        rsa_key = RSA.importKey(public_key)
        cipher = Cipher_pksc1_v1_5.new(rsa_key)
        cipher_text = base64.b64encode(cipher.encrypt(string.encode()))
        return cipher_text.decode()
