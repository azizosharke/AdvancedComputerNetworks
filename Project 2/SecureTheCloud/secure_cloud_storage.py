import json
import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from io import BytesIO

class SecureCloudStorage:

    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.email] = user

    def remove_user(self, user_email):
        if user_email in self.users:
            del self.users[user_email]
    def get_user(self, user_email):
        return self.users.get(user_email)        

    def encrypt_data(self, data, user_email):
        if user_email not in self.users:
            raise ValueError('User not found.')

        user = self.users[user_email]
        recipient_key = RSA.import_key(user.public_key)
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        encrypted_data = cipher_rsa.encrypt(data)
        return encrypted_data

    def decrypt_data(self, encrypted_data, user_email):
        if user_email not in self.users:
            raise ValueError('User not found.')

        user = self.users[user_email]
        private_key = RSA.import_key(user.private_key)
        cipher_rsa = PKCS1_OAEP.new(private_key)
        data = cipher_rsa.decrypt(encrypted_data)
        return data

    def upload_to_drive(self, user_email, file_path, encrypted_file_path):
        if user_email not in self.users:
            raise ValueError('User not found.')

        user = self.users[user_email]
        service = build('drive', 'v3', credentials=user.credentials)

        with open(file_path, 'rb') as f:
            data = f.read()

        encrypted_data = self.encrypt_data(data, user_email)

        with open(encrypted_file_path, 'wb') as f:
            f.write(encrypted_data)

        file_metadata = {'name': encrypted_file_path}
        media = MediaFileUpload(encrypted_file_path, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'File ID: "{file.get("id")}"')

        return file.get('id')

    def download_from_drive(self, user_email, file_id, decrypted_file_path):
        if user_email not in self.users:
            raise ValueError('User not found.')

        user = self.users[user_email]
        service = build('drive', 'v3', credentials=user.credentials)

        try:
            request = service.files().get_media(fileId=file_id)
            file = request.execute()

            decrypted_data = self.decrypt_data(file, user_email)

            with open(decrypted_file_path, 'wb') as f:
                f.write(decrypted_data)
                print(f'Decrypted file saved to {decrypted_file_path}')

        except HttpError as error:
            print(f'An error occurred: {error}')
            return None
