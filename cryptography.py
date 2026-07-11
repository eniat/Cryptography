from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes, hmac
from cryptography.hazmat.backends import default_backend
import os

def aes_encrypt(key, plaintext):
    plaintext = plaintext.encode("utf-8")
    # Generate an initialisation vector
    IV = os.urandom(16)
    # Generate padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    # Create the AES cipher in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(IV), backend=default_backend())
    # Create the encryptor object
    encryptor = cipher.encryptor()
    # Encrypt the plaintext
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return IV, ciphertext

def generate_hmac(key, data):
    # Creates a HMAC object with the hash chosen as SHA256
    HMAC = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    # Updates the data and finalizes the Hmac
    HMAC.update(data)
    MAC = HMAC.finalize()
    return MAC

def encrypt_then_mac(plaintext, aes_key, mac_key):
    # Calling the aes encrypt function
    IV, ciphertext = aes_encrypt(aes_key, plaintext)
    MAC = generate_hmac(mac_key, IV + ciphertext)
    return IV, ciphertext, MAC

def decrypt_and_verify(iv, ciphertext, mac, aes_key, mac_key):
    # Decrypt the ciphertext and verify the MAC.
    expected_mac = generate_hmac(mac_key, iv + ciphertext)
    if hmac.compare_digest(mac, expected_mac):
        # Create the AES cipher in CBC mode
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
        # Create the decryptor object
        decryptor = cipher.decryptor()
        # Decrypt the ciphertext
        message = decryptor.update(ciphertext) + decryptor.finalize()
        # Depad the message
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(message)
        plaintext += unpadder.finalize()
        plaintext = plaintext.decode("utf-8")
    else:
        raise ValueError
    return plaintext


# Basic functionality test.
if __name__ == "__main__":
    aes_key = os.urandom(32)
    mac_key = os.urandom(32)
    plaintext = "Basic func onality test"
    iv, ciphertext, mac = encrypt_then_mac(plaintext, aes_key, mac_key)
    decrypted_message = decrypt_and_verify(iv, ciphertext, mac, aes_key, mac_key)
    assert decrypted_message == plaintext
    print("Basic functionality test passed")

# Empty plaintext
if __name__ == "__main__":
    aes_key = os.urandom(32)
    mac_key = os.urandom(32)
    plaintext = ""
    iv, ciphertext, mac = encrypt_then_mac(plaintext, aes_key, mac_key)
    decrypted_message = decrypt_and_verify(iv, ciphertext, mac, aes_key, mac_key)
    assert decrypted_message == plaintext
    print("Empty plaintext test passed")

# Long plaintext
if __name__ == "__main__":
    aes_key = os.urandom(32)
    mac_key = os.urandom(32)
    plaintext = "M" * 10**6
    iv, ciphertext, mac = encrypt_then_mac(plaintext, aes_key, mac_key)
    decrypted_message = decrypt_and_verify(iv, ciphertext, mac, aes_key, mac_key)
    assert decrypted_message == plaintext
    print("Long plaintext test passed")

# Modified ciphertext test
if __name__ == "__main__":
    aes_key = os.urandom(32)
    mac_key = os.urandom(32)
    plaintext = "Modified ciphertext test"
    iv, ciphertext, mac = encrypt_then_mac(plaintext, aes_key, mac_key)
    modified_ciphertext = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0x01])
    try:
        decrypted_message = decrypt_and_verify(iv, modified_ciphertext, mac, aes_key, mac_key)
        print("Modified ciphertext test failed")
    except ValueError as e:
        print("Modified ciphertext test passed")

# Modified MAC test
if __name__ == "__main__":
    aes_key = os.urandom(32)
    mac_key = os.urandom(32)
    plaintext = "Modified MAC test"
    iv, ciphertext, mac = encrypt_then_mac(plaintext, aes_key, mac_key)
    modified_mac = mac[:-1] + bytes([mac[-1] ^ 0x01])
    try:
        decrypted_message = decrypt_and_verify(iv, ciphertext, modified_mac, aes_key, mac_key)
        print("Modified MAC test failed")
    except ValueError as e:
        print("Modified MAC test passed")
