import os
import json
import requests
from requests.auth import HTTPBasicAuth
from base64 import b64encode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

class Auth:
    """
    Anaplan Authentication
    """
    def __init__(self,tokenEndpoint):
        self.tokenEndpoint = tokenEndpoint

    def basicAuth(self, email, password):
        self.email = email
        self.password = password
        
        # get token
        res =  requests.post(self.tokenEndpoint,auth=HTTPBasicAuth(self.email,self.password)).json()
        if(res['status']=='SUCCESS'): return res['tokenInfo']
        else: return res['statusMessage']

    def certificateAuth(self, publicCertPath, privateCertPath):
        # Create header
        with open(publicCertPath,'r') as file:
            publicPemText = file.read()

        headers = {
            'Authorization': f'CACertificate {b64encode(publicPemText.encode("utf-8")).decode("utf-8")}',
            'Content-Type' : 'application/json',
        }

        # Create body
        randomBytes = os.urandom(150)
        encodedData = str(b64encode(randomBytes).decode('utf-8'))

        with open(privateCertPath, 'r') as file:
            privateKey = serialization.load_pem_private_key(file.read().encode('utf-8'),None,backend=default_backend())
        signature = privateKey.sign(randomBytes,padding.PKCS1v15(), hashes.SHA512())
        encodedSignedData = b64encode(signature).decode('utf-8')

        body = {
            'encodedData' : encodedData,
            'encodedSignedData' : encodedSignedData,
        }

        res = requests.post(self.tokenEndpoint,data=json.dumps(body),headers=headers).json()
        if(res['status']=='SUCCESS'): return res['tokenInfo']
        else: return res['statusMessage']
