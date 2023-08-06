from typing import Tuple, List

import grpc

import blindecdh
import pskca

import time

from cakes.proto import cakes_pb2_grpc as pb2_grpc, cakes_pb2 as pb2
from cakes.types import (
    ECDHVerificationCallback,
    CertificateIssuedCallback,
    RejectedByPeer,
    RejectedBySelf,
    EPERM,
    EWAIT,
)
from cakes.util import (
    unconditional_accept_cert,
    unconditional_accept_ecdh,
)

from cryptography.x509 import (
    Certificate,
    CertificateSigningRequest,
)
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
)


class CAKESClient(object):
    def __init__(
        self,
        channel: grpc.Channel,
        csr: CertificateSigningRequest,
        verification_callback: ECDHVerificationCallback,
        certificate_issued_callback: CertificateIssuedCallback,
    ) -> None:
        """Initializes the CAKES client.

        Parameters:
            channel: a grpc.Channel to talk to the server through.
            csr: a certificate signing request to be signed by the
            CAKES server.
            verification_callback: a callback which the ECDH exchange process
            will call to give your code an opportunity to accept or reject
            the result of an ECDH exchange.  The process does not move forward
            until your callback returns True.  If it returns False, the
            exception RejectedBySelf is raised in run().
            certificate_issued_callback: a callback issued prior to returning
            from the process (see function run()) that gives your code the
            opportunity to accept or reject the certificate.  If it returns
            False, the exception RejectedBySelf is raised in run().  This
            callback receives an empty peer name, the issued certificate, and
            a list (chain) of certificates that form the root of trust used
            to validate the identity of the authenticated server.
        """
        self.channel = channel
        self.csr = csr
        self.verification_callback = verification_callback
        self.cert_issued_callback = certificate_issued_callback

    def run(
        self,
        retry_interval: float = 3.0,
    ) -> Tuple[Certificate, List[Certificate]]:
        """Runs the CAKES protocol against the server connected to the channel.

        If the server provisionally accepts the ECDH exchange, then the
        verification_callback will be called (with an empty peer name and the
        completed ECDH exchange).  The callback can then decide whether the
        exchange is verified, and return True -- or reject the exchange,
        in which case it must return False (then this raises RejectedBySelf).

        At the end of a successful process, it returns the certificate issued
        to your code, as well as the certificate chain for the root of trust
        you can use to verify the authenticated server.

        If the server rejected the ECDH exchange or otherwise failed to perform
        the exchange or issue the cert, an exception RejectedByPeer is raised.

        If the certificate issuance callback return False, the exception
        RejectedBySelf is raised.

        If the communication was tampered between the parties, an exception
        pskca.CannotDecrypt will be raised.

        Parameters:
            retry_interval: (default 3) how many seconds to wait between
            retries when the server says that verification is still pending.
        """
        s = blindecdh.ECDHProtocol()
        stub = pb2_grpc.CAKESStub(self.channel)
        try:
            stub.ClientPubkey(
                pb2.ECDHKey(
                    pubkey=s.public_key.public_bytes(
                        serialization.Encoding.PEM,
                        serialization.PublicFormat.SubjectPublicKeyInfo,
                    )
                )
            )
            reply = stub.ServerPubkey(pb2.Ack()).pubkey
            remote_pubkey_pem = load_pem_public_key(reply)
        except grpc.RpcError as e:
            if e.code() == EPERM:
                raise RejectedByPeer(e.details())
            raise

        complete = s.run(remote_pubkey_pem)

        result = self.verification_callback("", complete)
        if not result:
            raise RejectedBySelf()

        psk = complete.derived_key

        requestor = pskca.Requestor(psk)

        request = pb2.IssueCertificateRequest(
            EncryptedCSR=requestor.encrypt_csr(self.csr).to_bytes()
        )

        retry = False
        while True:
            try:
                reply = stub.IssueCertificate(request)
            except grpc.RpcError as e:
                if e.code() == EPERM:
                    raise RejectedByPeer(e.details())
                elif e.code() == EWAIT:
                    retry = True
                else:
                    raise
            if retry:
                time.sleep(retry_interval)
            else:
                break

        cert, chain = requestor.decrypt_reply(
            pskca.EncryptedClientCertificate(reply.EncryptedClientCert),
            pskca.EncryptedCertificateChain(reply.EncryptedCertChain),
        )

        result = self.cert_issued_callback("", cert, chain)
        if not result:
            raise RejectedBySelf()

        return cert, chain


__all__ = ["CAKESClient"]


def __client() -> None:
    csr, unused_key = pskca.create_certificate_signing_request()
    with grpc.insecure_channel("127.0.40.50:50052") as channel:
        client = CAKESClient(
            channel,
            csr,
            unconditional_accept_ecdh,
            unconditional_accept_cert,
        )
        print("connecting client")
        one, two = client.run()
        print(one)
        print(two)
        print("done")


if __name__ == "__main__":
    __client()
