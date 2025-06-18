# 🔐 Secure Image & Message Transfer System
A Python-based system that securely encrypts, signs, and transmits messages along with compressed images using RSA and AES encryption techniques.
# 🚀 Overview
This project implements a secure communication pipeline between a sender and receiver that ensures:

* ✅ Confidentiality: AES-256 encrypted messages and images.

* ✍️ Authenticity: RSA digital signature to verify sender identity.

* 🔏 Integrity: Signature validation ensures message wasn’t tampered with.

* 📥 Compression: Images are compressed before transmission.

* 💬 Manual message support: Write custom text messages to send.

* 📁 File selection: Upload any image from your local device.

# 🧠 Key Concepts Used
* RSA (2048-bit) for asymmetric key encryption (used for encrypting AES keys and digital signatures).

* AES (256-bit CBC Mode) for encrypting the actual message and image payload.

* SHA256 for hashing the data during signature creation/verification.

* Digital Signatures to ensure authenticity of the message sender.
# 🧪 How to Use
* Generate keys
* Start the Server
* Start the Receiver (Bob)
* Run the Sender (Alice)
* Steps Followed
    * Sender selects an image and writes a message.

    * Image is compressed and both message & image are encrypted.

    * The encrypted AES key and payload are signed and sent via the server.

    * Receiver gets the data, verifies the signature, decrypts the message and image.
# 📦 Features
* 📁 Select any image from your local PC

* 🖼️ JPEG compression for efficient transfer

* 💬 Manual message input

* 🔒 RSA + AES hybrid encryption

* ✅ Digital signature verification

* 🧩 Clean modular code structure
# 📸 Output
* Sender Terminal
  ![image]()
* Receiver Terminal
  ![image]()
# 🔒 Security Considerations
* Uses modern and secure cryptographic standards.
* Any tampering with keys or data results in failed verification.
* Confidential information is only visible to authorized parties.

# 🤝 Contributions
Contributions, issues, and suggestions are welcome!!
# 👨‍💻 Author
Developed with ❤️ by Garima Kushwaha.
Feel free to contact me for collaboration or queries.
  
