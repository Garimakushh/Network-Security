# sender.py
import socket
from os import urandom, path
from PIL import Image
import io
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad
from tkinter import Tk, filedialog

def compress_image(input_path):
    print("[📥] Compressing image...")
    img = Image.open(input_path)
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=50)
    print("[✅] Image compressed.")
    return buffer.getvalue()

def load_public_key(filename): 
    with open(filename, "rb") as f:
        return RSA.import_key(f.read())

def load_private_key(filename):
    with open(filename, "rb") as f:
        return RSA.import_key(f.read())

# Load keys
public_key = load_public_key("keys/Bob_public.pem")
private_key = load_private_key("keys/Alice_private.pem")

# Select image file
Tk().withdraw()
image_path = filedialog.askopenfilename(title="Select Image to Send")
if not image_path:
    print("[❌] No image selected. Exiting.")
    exit()

original_size = path.getsize(image_path)
print(f"[📦] Original Image Size: {original_size} bytes")

img_data = compress_image(image_path)
compressed_size = len(img_data)
print(f"[🗜️] Compressed Image Size: {compressed_size} bytes")

# Ask user to input a message
print("\n📧 Compose your secure message:")
message_text = input("Type your message: ").encode()

# Combine message + image
combined_data = len(message_text).to_bytes(4, 'big') + message_text + img_data

# Encrypt using AES
print("[🔒] Encrypting with AES...")
aes_key = urandom(32)
iv = urandom(16)
cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
encrypted_payload = cipher_aes.encrypt(pad(combined_data, AES.block_size))
print(f"[🔐] Encrypted payload size: {len(encrypted_payload)} bytes")

# Sign the data
print("[✍️] Signing message and image...")
h = SHA256.new(combined_data)
signature = pkcs1_15.new(private_key).sign(h)
print(f"[✔️] Signature created. Length: {len(signature)} bytes")

# Encrypt AES key using receiver's public RSA key
cipher_rsa = PKCS1_OAEP.new(public_key)
enc_aes_key = cipher_rsa.encrypt(aes_key)

# Send to server
print("[📡] Connecting to server...")
HOST = 'localhost'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(enc_aes_key)
    s.sendall(iv)
    s.sendall(len(signature).to_bytes(4, 'big'))
    s.sendall(signature)
    s.sendall(len(encrypted_payload).to_bytes(8, 'big'))
    s.sendall(encrypted_payload)

print("[✅] Message and image sent to server.")
