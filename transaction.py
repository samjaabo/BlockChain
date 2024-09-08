from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import binascii
import json
import uuid

class ECDSAHandler:
    def __init__(self, curve='P-256'):
        self.curve = curve
        self.key = None
        self.private_key = None
        self.public_key = None
        self.new_keys(curve)

    def new_keys(self, curve='P-256'):
        self.key = ECC.generate(curve=curve)
        self.private_key = self.key.export_key(format='PEM', use_pkcs8=True)  # No need to decode
        self.public_key = self.key.public_key().export_key(format='PEM')  # No need to decode

    # 1. Export private key in Bitcoin format
    def export_private_key(self):
        # Convert PEM private key to raw DER format
        private_key_der = self.key.export_key(format='DER', use_pkcs8=True)
        # Convert DER to hex and truncate the leading bytes
        return binascii.hexlify(private_key_der[7:]).decode()  # Remove DER header

    # 2. Export public key in Bitcoin compressed format
    def export_public_key(self):
        public_key = self.key.public_key().export_key(format='DER')
        x = public_key[0x12:0x12+32]
        y = public_key[0x12+32:0x12+64]
        prefix = b'\x02' if y[0] % 2 == 0 else b'\x03'
        return binascii.hexlify(prefix + x).decode()

    # 3. Import private key from Bitcoin format
    def import_private_key(self, private_key_hex):
        private_key_der = b'\x30\x81\x87\x02\x01\x01\x30\x13\x06\x07\x2a\x86\x48\xce\x3d\x02\x01\x06\x08\x2a\x86\x48\xce\x3d\x03\x01\x07\x04\x6d\x30\x6b\x02\x01\x01\x04\x20' + binascii.unhexlify(private_key_hex)
        self.key = ECC.import_key(private_key_der, format='DER', use_pkcs8=True)
        self.private_key = self.key.export_key(format='PEM', use_pkcs8=True)

    # 4. Import public key from Bitcoin format
    def import_public_key(self, public_key_hex):
        public_key_der = binascii.unhexlify(public_key_hex)
        self.key = ECC.import_key(public_key_der, format='DER')
        self.public_key = self.key.public_key()

    # 5. Sign message and return signature as hex
    def sign(self, message):
        if isinstance(message, str):
            message = message.encode()
        h = SHA256.new(message)
        signature = DSS.new(self.key, 'fips-186-3').sign(h)
        return binascii.hexlify(signature).decode()

    # 6. Verify signature from hex
    def verify(self, message, signature_hex):
        if isinstance(message, str):
            message = message.encode()
        signature = binascii.unhexlify(signature_hex)
        h = SHA256.new(message)
        try:
            DSS.new(self.key.public_key(), 'fips-186-3').verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

# Example usage
# if __name__ == "__main__":
#     # Initialize ECDSAHandler
#     ecdsa_handler = ECDSAHandler()
#     # Generate new keys
#     ecdsa_handler.new_keys()
#     # Export keys as hex
#     private_key_hex = ecdsa_handler.export_private_key()
#     public_key_hex = ecdsa_handler.export_public_key()
#     print("Private Key (Bitcoin format):", private_key_hex)
#     print("Public Key (Bitcoin format):", public_key_hex)
#     exit(0)

import hashlib
import base58

def public_key_to_address(public_key_hex):
    # Step 1: Convert hex public key to bytes
    public_key_bytes = bytes.fromhex(public_key_hex)

    # Step 2: Perform SHA-256 hashing
    sha256_hash = hashlib.sha256(public_key_bytes).digest()

    # Step 3: Perform RIPEMD-160 hashing
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()

    # Step 4: Add network byte (0x00 for mainnet)
    network_byte = b'\x00' + ripemd160_hash

    # Step 5: Perform SHA-256 hashing twice
    checksum = hashlib.sha256(hashlib.sha256(network_byte).digest()).digest()[:4]
    print((network_byte + checksum).hex())
    # Step 6: Append checksum and encode in Base58
    address = base58.b58encode(network_byte + checksum).decode()

    return address

# Example usage
public_key_hex = '02ce3d03010703420004933bf495067ddebf0f0f5572c0c3f8c18fd26c60faaa40'
address = public_key_to_address(public_key_hex)
print("Bitcoin Address:", address)

