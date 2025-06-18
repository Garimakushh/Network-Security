# keygen.py
from Crypto.PublicKey import RSA
import os

KEY_DIR = "keys"
os.makedirs(KEY_DIR, exist_ok=True)

def generate_keys(name):
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open(f"{KEY_DIR}/{name}_private.pem", "wb") as f:
        f.write(private_key)
    with open(f"{KEY_DIR}/{name}_public.pem", "wb") as f:
        f.write(public_key)

    print(f"[🔑] Keys generated for {name}.")

def main():
    generate_keys("Alice")  # Sender
    generate_keys("Bob")    # Receiver
    print("[✅] All keys generated and saved in 'keys/' directory.")

if __name__ == "__main__":
    main()
