"""
Disclaimer:

Please note that I am only learning about Web3
and blockchain technology, and my involvement is purely for educational purposes.
I do not engage in any illegal activities.
and I fully comply with the laws and regulations of Morocco.
"""


import base58
import ecdsa
from ecdsa import SigningKey, SECP256k1
from hashlib import sha256, new as new_hash

class Wallet:
    def __init__(self, private_key=None):
        if private_key:
            self.private_key = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
        else:
            self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
        self.private_key_wif = self._private_key_to_wif(self.private_key)
        self.compressed_public_key = self._public_key_to_compressed(self.public_key)
        self.bitcoin_address = self._public_key_to_address(self.compressed_public_key)

    def _private_key_to_wif(self, private_key):
        # Convert private key to WIF (Wallet Import Format)
        private_key_bytes = b'\x80' + private_key.to_string()  # Add version byte (0x80) for mainnet
        private_key_hash = sha256(private_key_bytes).digest()
        private_key_hash = sha256(private_key_hash).digest()
        private_key_hash = private_key_hash[:4]  # Get the first 4 bytes of the hash for checksum
        wif = base58.b58encode(private_key_bytes + private_key_hash).decode()
        return wif

    def _public_key_to_compressed(self, public_key):
        # Convert public key to compressed format
        pub_key_bytes = public_key.to_string()
        if pub_key_bytes[0] % 2 == 0:
            return b'\x02' + pub_key_bytes[1:]
        else:
            return b'\x03' + pub_key_bytes[1:]

    def _public_key_to_address(self, compressed_public_key):
        # Convert compressed public key to Bitcoin address
        pub_key_hash = sha256(compressed_public_key).digest()
        ripemd160 = new_hash('ripemd160')
        ripemd160.update(pub_key_hash)
        pub_key_hash = ripemd160.digest()
        address_bytes = b'\x00' + pub_key_hash  # Add version byte (0x00) for mainnet
        address_hash = sha256(address_bytes).digest()
        address_hash = sha256(address_hash).digest()
        address_hash = address_hash[:4]  # Get the first 4 bytes of the hash for checksum
        address = base58.b58encode(address_bytes + address_hash).decode()
        return address

    def export_private_key(self):
        return self.private_key_wif

    def export_public_key(self):
        return self.compressed_public_key.hex()

    def __str__(self):
        return (f"Private Key (WIF format): {self.private_key_wif}\n"
                f"Compressed Public Key:    {self.compressed_public_key.hex()}\n"
                f"Bitcoin Address:          {self.bitcoin_address}")

# Example usage
if __name__ == "__main__":
    wallet = Wallet()
    print(wallet)

    # Test importing a wallet from a WIF private key
    wallet_from_wif = Wallet(private_key=wallet.private_key.to_string().hex())
    print("\nImported wallet details:")
    print(wallet_from_wif)
