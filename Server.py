# server.py
import socket

HOST = 'localhost'
SENDER_PORT = 12345
RECEIVER_PORT = 12346

def main():
    print("[🖥️] Secure Image Transfer Server Starting...")

    # Connect to Receiver
    print("[📥] Waiting for receiver to connect...")
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recv_sock.bind((HOST, RECEIVER_PORT))
    recv_sock.listen(1)
    conn_receiver, addr_r = recv_sock.accept()
    print(f"[✅] Receiver connected from {addr_r}")
    recv_sock.close()

    # Connect to Sender
    print("[📤] Waiting for sender to connect...")
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_sock.bind((HOST, SENDER_PORT))
    send_sock.listen(1)
    conn_sender, addr_s = send_sock.accept()
    print(f"[✅] Sender connected from {addr_s}")
    send_sock.close()

    # Relay Data
    print("[🔄] Relaying data from sender to receiver...")
    while True:
        data = conn_sender.recv(4096)
        if not data:
            break
        conn_receiver.sendall(data)

    conn_sender.close()
    conn_receiver.close()
    print("[✅] Transfer complete.")

if __name__ == "__main__":
    main()
