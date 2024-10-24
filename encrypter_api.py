# from flask import Flask, request, jsonify
# from Crypto.Cipher import AES
# from Crypto.Protocol.KDF import PBKDF2
# import base64
# import os
# import xml.etree.ElementTree as ET
#
# app = Flask(__name__)
#
#
# # AES encryption key generation using PBKDF2
# def generate_key():
#     password = b'mysecretpassword'  # Use a strong password
#     salt = os.urandom(16)
#     key = PBKDF2(password, salt, dkLen=32)
#     return key, salt
#
#
# def encrypt_data(data, key):
#     cipher = AES.new(key, AES.MODE_GCM)
#     ciphertext, tag = cipher.encrypt_and_digest(data.encode())
#     return base64.b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')
#
#
# # Function to extract text from XML elements
# def extract_xml_text(xml_data):
#     try:
#         root = ET.fromstring(xml_data)
#         # Collect all text data from all nodes in the XML
#         return ''.join(root.itertext()).strip()
#     except ET.ParseError:
#         return None
#
#
# # Function to handle different content types
# def process_request_data():
#     if request.content_type == 'application/json':
#         data = request.json.get('data')
#     elif request.content_type == 'application/xml':
#         xml_data = request.data
#         data = extract_xml_text(xml_data)
#     else:
#         data = request.data.decode('utf-8')  # Handle plain text
#
#     if not data:
#         return None, 'No valid data provided'
#
#     return data, None
#
#
# @app.route('/encrypt', methods=['POST'])
# def encrypt():
#     data, error = process_request_data()
#
#     if error:
#         return jsonify({'error': error}), 400
#
#     key, _ = generate_key()
#     encrypted_data = encrypt_data(data, key)
#     return jsonify({'encrypted_data': encrypted_data})
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
# -----------------------------------

from flask import Flask, request, jsonify
import base64
from Crypto.Cipher import AES

app = Flask(__name__)

# Encryption parameters
SECRET_KEY = b'k92ldahavl97s428vxri7x89seoy79sm'
INIT_VECTOR = b'7dzhcnrb0016hmj3'

def encrypt_data(data):
    cipher = AES.new(SECRET_KEY, AES.MODE_GCM, nonce=INIT_VECTOR)
    ciphertext, auth_tag = cipher.encrypt_and_digest(data.encode())
    encrypted_data = ciphertext + auth_tag
    return base64.b64encode(encrypted_data).decode()

@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        # Get the input data from the request
        input_data = request.json.get('data')

        if not input_data:
            return jsonify({"error": "No data provided"}), 400

        # Encrypt the input data
        encrypted_data = encrypt_data(input_data)

        return jsonify({"encrypted_data": encrypted_data}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5003, debug=True)