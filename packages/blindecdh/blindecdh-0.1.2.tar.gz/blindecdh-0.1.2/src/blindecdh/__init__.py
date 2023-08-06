"""
This package implements unauthenticated ECDH between two endpoints.
Authentication can then later be added by, for example, mutual short string
authentication (as exemplified by the simpleauthstrings package).

The exchange happens by using the ECDHProtocol on both sides, exchanging the
peer public key of one instance with the other, and viceversa.  Completed
exchange returns a CompletedECDH instance.

Unless both sides of the ECDH exchange, you must not use the derived or shared
keys on the CompletedECDH instances to perform cryptography — otherwise you
will be vulnerable to an active man-in-the-middle attack.

This is mostly based on
https://medium.com/asecuritysite-when-bob-met-alice/ecdh-using-python-and-hazmat-39d5b94b2e15  # noqa

"""

from typing import Optional
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePrivateKey,
    EllipticCurvePublicKey,
)


__version__ = "0.1.2"


HKDF_SIZE = 32  # 256 bit HKDF


class CompletedECDH(object):
    """
    Represents a completed ECDH exchange.

    Attributes:
        private_key: the private key used by the ECDH protocol
        public_key: the public key corresponding to that private key
        shared_key: the key built by both ends after ECDH
        derived_key: a SHA256 HKDF derivation based on the shared key -
        this is what you probably should be using to initialize encrypted
        communications (of course, after verifying that both sides have
        the same derived key)
    """

    @property
    def public_key(self) -> EllipticCurvePublicKey:
        return self.private_key.public_key()

    def __init__(
        self,
        private_key: EllipticCurvePrivateKey,
        shared_key: bytes,
        derived_key: bytes,
    ):
        self.private_key = private_key
        self.shared_key = shared_key
        self.derived_key = derived_key


class ECDHProtocol(object):
    """
    Implements both sides of the ECDH key exchange.

    Specifying your own keys is optional in the ECDHProtocol instantiation.
    If not specified, by default a private key will be generated that uses
    the Bitcoin elliptic curve.
    """

    def __init__(self, private_key: Optional[EllipticCurvePrivateKey] = None) -> None:
        """
        Initialize the exchange protocol.

        You must supply an EllipticCurvePrivateKey.
        """
        if private_key is None:
            private_key = ec.generate_private_key(ec.SECP256K1())
        self.private_key = private_key

    @property
    def public_key(self) -> EllipticCurvePublicKey:
        """
        Obtain the public key associated to the private key of this side
        of the ECDH exchange.
        """
        return self.private_key.public_key()

    def run(self, peer_pubkey_pem: EllipticCurvePublicKey) -> CompletedECDH:
        """
        Run the ECDH exchange.

        You must supply the public key of the peer.

        Returns a CompletedECDH object.
        """
        public_key = peer_pubkey_pem
        shared_key = self.private_key.exchange(
            ec.ECDH(),
            public_key,
        )
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=HKDF_SIZE,
            salt=None,
            info=b"",
        ).derive(shared_key)

        return CompletedECDH(self.private_key, shared_key, derived_key)


__all__ = [ECDHProtocol.__name__, CompletedECDH.__name__]
