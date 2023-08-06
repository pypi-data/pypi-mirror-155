"""
Certificate authority kit, ECDH-powered, SAS-authenticated.

This package is a kit to build mutually-authenticated secure services.
You will find this package useful if:

* You have a server program, and a client program.
* You want to secure communications between these programs using SSL
  or gRPC secure channels.
* You do not have a certificate authority or other PKI system on hand.
* All you need is a way to authenticate the client on the server side,
  and the server on the client side.
* You want to authenticate the two parts by making a visual comparison
  on both sides (much like Bluetooth PIN pairing).

The way you use this goes more or less as explained here:

Step 1: make your server run a CAKESServicer on an insecure gRPC channel.

```
# Create a dummy CA cert with the power to issue certificates.
# You can use an actual CA cert or a CA cert delegated by a
# root cert.
ca_cert, ca_key = pskca.create_certificate_and_key(
    ca=True,
    cn="dummy.not.for.production"
)
# Create the CA object that will issue certs.
# The third parameter is going to be the chain of certificates that
# the client will be given to trust, so it does not have to be the
# CA cert itself.
ca = pskca.CA(ca_cert, ca_key, [ca_cert])
# Create your gRPC server.
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
# Create the CAKESServicer and add some callbacks to authenticate
pb2_grpc.add_CAKESServicer_to_server(
    cakes.CAKESServicer(
        ca,
        accept_ecdh,
        cakes.unconditional_accept_cert,
    ),
    server,
)
# Add insecure port to your server.
server.add_insecure_port("0.0.0.0:50052")
# Start and wait.
server.start()
server.wait_for_termination()
```

Step 2: make your client adopt a CAKESClient to obtain its certificate.

```
# Generate dummy certificate signing request.
csr, client_key = pskca.create_certificate_signing_request()
# Create gRPC insecure channel.
with grpc.insecure_channel("localhost:50052") as channel:
    client = cakes.CAKESClient(
        channel,
        csr,
        accept_ecdh,
        cakes.unconditional_accept_cert,
    )
    client_cert, chain = client.run()
```

Step 3: provide an authentication function.

You'll note that in both steps above there's an `accept_ecdh` function in use.
You supply this function; both the client and the server will call it with
the name of the peer, and an object of class blindecdh.CompletedECDH.  This
object has an attribute `derived_key` that is a 32-byte array.  You can then
make your `accept_ecdh` function print or display a simplified version of the
key, and ask if the exchange is accepted:

```
def accept_ecdh(peer, completed_ecdh):
    from shortauthstrings import emoji
    s = emoji(completed_ecdh.derived_key)
    print("Peer %s says he has key %s.  Accept?  [Y/N then ENTER]" % (peer, s))
    response = sys.stdin.readline()
    if response.lower().startswith("y"):
        return True
    return False
```

Step 4: use the CA / signing certificate on the server

Once the client has received its certificate, then the server and the client
can talk in the customary way.  The server needs to use a certificate either
signed by the CA you used in step 1, or the same certificate.  Effectively,
the server has to use a certificate that is in the chain of trust given to
the client in step #2.

```
# server side
...
credentials = grpc.ssl_server_credentials(
    (
        (
            ca_cert.public_bytes(serialization.Encoding.PEM),
            ca_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            ),
        ),
    ),
    PEM.from_rsa_certificate(root_cert).as_bytes(),
    require_client_auth=True,
)
server.add_secure_port("0.0.0.0:50051", credentials)
...
```

Step 5: use the obtained certificate on the client.

```
# client side
pem_chain = "\n".join([
    c.public_bytes(serialization.Encoding.PEM)
    for c in chain
])
pem_client_key = client_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption(),
)
pem_client_cert = client_cert.public_bytes(
    serialization.Encoding.PEM
)
credentials = grpc.ssl_channel_credentials(
    pem_chain,
    pem_client_key,
    pem_client_cert,
)
# We must override the target name so the server chooses
# the right certificate to present to us, irrespective
# of the actual DNS or IP address used.  Since we forced the CN
# of the CA certificate, and we're reusing the CA certificate as
# the server certificate, this will work.
server_cert_hostname = "dummy.not.for.production"
server_hostname = "127.0.0.1"
channel = grpc.secure_channel(
    "%s:50051" % server_hostname,
    credentials,
    options=[("grpc.ssl_target_name_override", server_cert_hostname)],
)
stub = myservice_pb2_grpc.MyServiceServiceStub(channel=channel)
# This call is now encrypted using SSL and mutually authenticated.
stub.my_function()
...
```

How does this work?  It's fairly simple.

1. The client talks over the insecure port to the server, initiating
   an ECDH exchange.
2. The server cooperates with the client in the ECDH exchange.
3. Both sides ask the user for authentication, which uses a visually
   easy-to-use representation (we recommend using package `shortauthstrings`)
   to display to the user what the resulting ECDH key was.
4. Once both sides are verified, we know there's no man-in-the-middle
   attack, and the second part happens.  The client encrypts its CSR
   using the agreed key and sends it to the server.
5. The server decrypts the CSR with the agreed key, and signs it, returning
   to the client an encrypted certificate as well as an encrypted chain
   of trust.
6. The client receives these values, then decrypts them.
7. Server and client may now begin using these newly-agreed-upon certificate
   materials to do actual mutually-authenticated SSL.
   (Technically speaking, if the CA cert is used for the CA object, and the
   CA cert also issues the server certificate, the secure service may start
   -- using the server certificate -- before any client certificate is
   issued.  So long as the chain of trust passed to the CA object is correct,
   then any client which later gets certificates issued should just work by
   using those certificates issued to them.)
"""

# FIXME: we also need a schematic of how the thing works and how the
# certs relate to each other.

from cakes.client import CAKESClient  # noqa: F401
from cakes.server import CAKESServicer  # noqa: F401
from cakes.util import (  # noqa: F401
    unconditional_accept_cert,
    unconditional_accept_ecdh,
)

from cakes.types import (  # noqa: F401
    CannotDecrypt,
    RejectedBySelf,
    Rejected,
    RejectedByPeer,
    ECDHVerificationCallback,
    CertificateIssuedCallback,
)

__version__ = "0.0.3"

__all__ = [
    "unconditional_accept_cert",
    "unconditional_accept_ecdh",
    "CannotDecrypt",
    "Rejected",
    "RejectedBySelf",
    "RejectedByPeer",
    "ECDHVerificationCallback",
    "CertificateIssuedCallback",
    "CAKESClient",
    "CAKESServicer",
]
