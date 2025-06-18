# receiver.py
import socket
from PIL import Image
import io
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad

def load_private_key(filename):
    with open(filename, "rb") as f:
        return RSA.import_key(f.read())

def load_public_key(filename):
    with open(filename, "rb") as f:
        return RSA.import_key(f.read())

def decompress_image(byte_data, output_path="received_image.jpg"):
    print("[🧼] Decompressing image...")
    buffer = io.BytesIO(byte_data)
    img = Image.open(buffer)
    img.save(output_path)
    print(f"[💾] Image saved as '{output_path}'")

HOST = 'localhost'
PORT = 12346  # Port to connect to server

print("[🔌] Connecting to server...")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("[🔗] Connected to server.")

    # Load keys
    private_key = load_private_key("keys/Bob_private.pem")
    sender_public_key = load_public_key("keys/Alice_public.pem")

    # Receive encrypted AES key
    encrypted_key = s.recv(256)
    aes_key = PKCS1_OAEP.new(private_key).decrypt(encrypted_key)

    # Receive IV
    iv = s.recv(16)

    # Receive Signature
    sig_len = int.from_bytes(s.recv(4), 'big')
    signature = s.recv(sig_len)

    # Receive Encrypted Payload
    payload_len = int.from_bytes(s.recv(8), 'big')
    encrypted_payload = b""
    while len(encrypted_payload) < payload_len:
        chunk = s.recv(2048)
        if not chunk:
            break
        encrypted_payload += chunk

print("[🔐] Decrypting payload...")
cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
combined_data = unpad(cipher_aes.decrypt(encrypted_payload), AES.block_size)

# Split message and image
msg_len = int.from_bytes(combined_data[:4], 'big')
message_text = combined_data[4:4+msg_len].decode()
image_data = combined_data[4+msg_len:]

# Verify Signature
print("[🔍] Verifying signature...")
h = SHA256.new(combined_data)
try:
    pkcs1_15.new(sender_public_key).verify(h, signature)
    print("[✅] Signature verified.")
    print(f"\n📨 Received Secure Message:\n\"{message_text}\"\n")
except (ValueError, TypeError):
    print("[❌] Signature verification failed.")
    exit()

# Save image
decompress_image(image_data)
