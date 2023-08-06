from typing import Optional
import blindecdh
import pskca

import threading
import grpc
from cakes.proto import cakes_pb2_grpc as pb2_grpc, cakes_pb2 as pb2
from cakes.types import (
    ECDHVerificationCallback,
    CertificateIssuedCallback,
    EPERM,
    EWAIT,
    EINVAL,
)
from cakes.util import (
    unconditional_accept_cert,
    unconditional_accept_ecdh,
)


from pskca.util import TimedDict

from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
)
from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePublicKey,
)


# FIXME prevent abuse by forcing the client to do
# an expensive computation.


class CAKESServicer(pb2_grpc.CAKESServicer):
    def __init__(
        self,
        ca: pskca.CA,
        verification_callback: ECDHVerificationCallback,
        certificate_issued_callback: CertificateIssuedCallback,
    ):
        """
        Initializes the CAKES servicer.

        This gRPC servicer provides services to CAKES clients.

        All you must bring to the table is a callback function that, when
        called, shows an authorization request to the user, and if responded
        in the affirmative by him, returns True.

        Parameters:
            ca: a `pskca.CA` object.
            verification_callback: a callback to call with the peer
            identification and the completed ECDH to further process down the
            line.  After completed ECDH, the callback function will be called,
            so your code must use that callback function to authenticate that
            the client identity matches (e.g. via short authentication strings,
            as per the shortauthstrings package).
            certificate_issued_callback: a callback that will be called with
            the peer and the issued certificate every time a certificate is
            issued.  If this callback does not return True, the certificate is
            denied to the client.
        """
        p: TimedDict[str, Optional[EllipticCurvePublicKey]] = TimedDict(60, 4)
        self.peers = p
        self.ca = ca
        self.callback = verification_callback
        self.cert_issued_callback = certificate_issued_callback

    def ClientPubkey(
        self, request: pb2.ECDHKey, context: grpc.ServicerContext
    ) -> pb2.Ack:
        """
        Retrieves the public key of the ECDH exchange from the client.

        This is the first step in CAKES.
        """
        peer: str = context.peer()
        with self.peers:
            if peer in self.peers:
                context.abort(EPERM, "an ECDH is already ongoing")
        k = load_pem_public_key(request.pubkey)
        if not isinstance(k, EllipticCurvePublicKey):
            context.abort(EINVAL, "not a valid public key")
        self.peers[peer] = k
        return pb2.Ack()

    def ServerPubkey(
        self, request: pb2.Ack, context: grpc.ServicerContext
    ) -> pb2.ECDHKey:
        """
        Sends the public key of the ECDH exchange to the client.

        This is the second step in CAKES.

        At the end of this process, after the public key has been
        returned to the client, the callback function is called
        (in a separate thread, so keep thread safety in mind).

        If that function returns True, then the client may invoke
        the next step in CAKES -- the IssueCertificate RPC call.
        """
        peer: str = context.peer()
        with self.peers:
            try:
                peer_pubkey = self.peers[peer]
                self.peers[peer] = None
            except KeyError:
                context.abort(EPERM, "unknown ECDH")
                return
        if peer_pubkey is None:
            context.abort(EPERM, "an ECDH is already ongoing")
            return

        s = blindecdh.ECDHProtocol()
        if not isinstance(
            peer_pubkey,
            s.public_key.__class__,
        ):
            context.abort(
                EINVAL,
                "the curve of the ECDH exchange is wrong (%s != %s)"
                % (peer_pubkey.__class__, s.public_key.__class__),
            )
            return
        complete = s.run(peer_pubkey)

        def accept(peer: str, complete: blindecdh.CompletedECDH) -> None:
            self.ca.add_psk(peer, None)
            if self.callback(peer, complete):
                self.ca.add_psk(peer, complete.derived_key)

        t = threading.Thread(
            target=accept,
            args=(
                peer,
                complete,
            ),
            daemon=True,
        )
        t.start()
        return pb2.ECDHKey(
            pubkey=s.public_key.public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

    def IssueCertificate(
        self,
        request: pb2.IssueCertificateRequest,
        context: grpc.ServicerContext,
    ) -> pb2.IssueCertificateReply:
        """
        Issues a certificate to authorized clients.

        A client is authorized if:

        1. It has completed the ECDH phase (ClientPubkey + ServerPubkey)
        2. During ServerPubkey, the callback attached to this class returned
           True.
        3. At the time of calling this, the certificate_issued_callback
           is called, and the return value of the call is True.  Note that
           the call is blocking, so the client will not receive a response
           until and unless the callback is finished.

        The client must call this with an encrypted payload.  The payload
        must contain its certificate request, and must be encrypted with the
        derived_key of the CompletedECDH object on its side, which it obtains
        after successfully completing the ServerPubkey phase of the CAKES
        protocol.

        A reply to authenticated clients includes a message with two payloads:

        1. The issued certificate.  A newly-issued certificate, signed by
           the `pskca.CA` object, which the caller may use to do mutual TLS
           via gRPC or mTLS to any services protected by certificates signed
           by the CA (or the CA certificate itself).
        2. A chain of trust (derived from the `pskca.CA` object) to be sent
           to the client for purposes of authenticating against the
           authenticated service that the issued certificate is for.

        Replies to unsuccessful clients generally involve the gRPC status code
        PERMISSION_DENIED.

        If a client has completed the ECDH phase but the server has not yet
        finished authorizing the client's ECDH, the client will receive a reply
        with gRPC status code UNAUTHENTICATED.  The client should retry in a
        few seconds.
        """
        peer: str = context.peer()
        try:
            cert, chain, enc_cert, enc_chain = self.ca.issue_certificate(
                peer,
                pskca.EncryptedCertificateRequest(request.EncryptedCSR),
            )
        except pskca.UnknownRequestor:
            context.abort(EPERM, "no corresponding ECDH")
            return
        except pskca.Pending:
            context.abort(
                EWAIT,
                "the user has not yet approved the ECDH exchange",
            )
            return
        except pskca.CannotDecrypt:
            context.abort(
                EPERM,
                "cannot decrypt certificate signing request",
            )
            return

        cb_return = self.cert_issued_callback(peer, cert, chain)
        if not cb_return:
            context.abort(EPERM, "server denied certificate")
            return

        response = pb2.IssueCertificateReply(
            EncryptedClientCert=enc_cert.to_bytes(),
            EncryptedCertChain=enc_chain.to_bytes(),
        )
        return response


__all__ = ["CAKESServicer"]


def __server() -> None:
    from concurrent import futures

    cert, key = pskca.create_certificate_and_key(ca=True)
    ca = pskca.CA(cert, key, [cert])
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_CAKESServicer_to_server(
        CAKESServicer(
            ca,
            unconditional_accept_ecdh,
            unconditional_accept_cert,
        ),
        server,
    )

    server.add_insecure_port("127.0.40.50:50052")
    print("starting server")
    server.start()
    server.wait_for_termination()
    print("server ended")


if __name__ == "__main__":
    __server()
