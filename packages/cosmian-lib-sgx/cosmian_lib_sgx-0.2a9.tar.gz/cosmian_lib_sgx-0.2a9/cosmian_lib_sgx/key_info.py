"""cosmian_lib_sgx.key_info module."""

from hashlib import sha3_256
from pathlib import Path

from cosmian_lib_sgx.crypto_lib import verify, recover_psk
from cosmian_lib_sgx.error import CryptoError


class KeyInfo:
    """KeyInfo class for participant key.

    Parameters
    ----------
    pubkey: bytes
        Bytes of an Ed25519 public key.
    seal_box: bytes
        Sealed symmetric key for the enclave.

    Attributes
    ----------
    pubkey: bytes
        Bytes of an Ed25519 public key.
    fingerprint: str
        Public key fingerprint as the 8 lowest bytes of SHA3-256(pubkey).
    seal_box: bytes
        Sealed symmetric key for the enclave with attached signature.

    """

    def __init__(self, computation_uuid: bytes, pubkey: bytes, seal_box: bytes):
        """Init constructor of KeyInfo."""
        self.computation_uuid: bytes = computation_uuid
        self.pubkey: bytes = pubkey
        self.fingerprint: str = sha3_256(self.pubkey).digest()[-8:].hex()
        # (sig = Sig(computation_uuid (16) || seal_box (96), secretkey(pubkey)),
        #  seal_box = SealBox(psk (32) || symkey(32), enclave_pk))
        self.sig, self.seal_box = seal_box[:64], seal_box[64:]  # type: bytes, bytes

        msg: bytes = self.computation_uuid + self.seal_box
        try:
            m = verify(msg, self.sig, self.pubkey)
            if m != msg:
                raise CryptoError(f"Expected message {msg.hex()}, found {m.hex()}")
        except CryptoError as exc:
            raise CryptoError(
                f"Failed to verify sig {self.sig.hex()} with pk {self.pubkey.hex()}"
            ) from exc

        self.psk: bytes = recover_psk(self.sig + self.seal_box,
                                      self.computation_uuid,
                                      self.pubkey)

    @classmethod
    def from_path(cls, computation_uuid: bytes, path: Path):
        """Extract KeyInfo from a path."""
        hexa: str
        # hexadecimal string of the public key
        hexa, *_ = path.stem.split(".")
        # hex string to bytes
        pubkey: bytes = bytes.fromhex(hexa)
        # read file content for the sealed symmetric key
        seal_box: bytes = path.read_bytes()

        return cls(computation_uuid, pubkey, seal_box)
