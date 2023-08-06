# A simple implementation of unauthenticated ECDH

This package implements unauthenticated ECDH (the Elliptic Curve
Diffie-Hellman key agreement protocol) between two endpoints.  After the
exchange is complete, you can then add authentication to verify that both
parties are who they say they are — for example, mutual short string
authentication by displaying a derivative of the key (derived key) to
both parties, as exemplified by the
[simpleauthstrings](https://github.com/Rudd-O/simpleauthstrings) package.

Here is a sample with working code:

```
from blindecdh import ECDHProtocol
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
)


def pubkey_to_pem(pubkey):
    return pubkey.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def pem_to_pubkey(pem):
    return load_pem_public_key(pem)


# ------------------------

# Alice's side.

## Instantiate the protocol.
alice = ECDHProtocol()

## Serialize and send Alice's public key.
## The specific communications mechanism is omitted for brevity.
## We assume both parties traffic in PEM-encoded certificates.
bob_socket.send(pubkey_to_pem(alice.public_key))

## Get and deserialize Bob's public key.
bobs_public_key = pem_to_pubkey(bob_socket.receive())

## Compute the result.
result = alice.run(bobs_public_key)

## Display the derived key.  It will match Bob's.
print(result.derived_key)

# -----------------------

# Bob's side.

bob = ECDHProtocol()

## Get and deserialize Alice's public key.
## On Bob's side we do the send first, but here we receive first.
alices_public_key = pem_to_pubkey(alice_socket.receive())

## Serialize and send Bob's public key.
alice_socket.send(pubkey_to_pem(bob.public_key))

## Compute the result.
result = bob.run(alices_public_key)

## Display the derived key.  It will match Bob's.
print(result.derived_key)
```

See [module](src/blindecdh/__init__.py) for developer documentation.

This package is distributed under the GNU Lesser General Public License v2.1.
For relicensing, contact the package author.
