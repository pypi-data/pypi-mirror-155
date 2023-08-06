from typing import List
import os
import random
import sys
import tempfile

import grpc
import pskca

from cryptography.x509 import Certificate
from cryptography.hazmat.primitives import serialization

import cakes
from cakes.proto import cakes_pb2_grpc
from concurrent import futures


import subprocess


def verify_cert(chain: List[Certificate], cert: Certificate) -> None:
    with tempfile.TemporaryDirectory() as x:
        signer_path = os.path.join(x, "signer.crt")
        cert_path = os.path.join(x, "cert.crt")
        with open(signer_path, "wb") as f:
            for c in chain:
                f.write(c.public_bytes(serialization.Encoding.PEM))
                f.write(b"\n")
        with open(cert_path, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        subprocess.run(
            [
                "openssl",
                "verify",
                "-verbose",
                "-show_chain",
                "-trusted",
                signer_path,
                cert_path,
            ],
            capture_output=True,
            universal_newlines=True,
            check=True,
        )


def random_port() -> int:
    ports = list(range(1025, 65536))
    return random.choice(ports)


def random_ip() -> str:
    ips = list(range(0, 255))
    return "127.%s.%s.%s" % (
        random.choice(ips),
        random.choice(ips),
        random.choice(ips),
    )


def random_address() -> str:
    return random_ip() + ":" + str(random_port())


def test_protocol() -> None:
    address = random_address()
    print("Using address %s" % address, file=sys.stderr)
    cacert, key = pskca.create_certificate_and_key(ca=True)
    ca = pskca.CA(cacert, key, [cacert])
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cakes_pb2_grpc.add_CAKESServicer_to_server(
        cakes.CAKESServicer(
            ca,
            cakes.unconditional_accept_ecdh,
            cakes.unconditional_accept_cert,
        ),
        server,
    )
    server.add_insecure_port(address)
    server.start()

    try:
        csr, unused_key = pskca.create_certificate_signing_request()
        with grpc.insecure_channel(address) as channel:
            client = cakes.CAKESClient(
                channel,
                csr,
                cakes.unconditional_accept_ecdh,
                cakes.unconditional_accept_cert,
            )
            clientcert, chain = client.run()
            try:
                verify_cert(chain, clientcert)
            except subprocess.CalledProcessError as e:
                assert 0, (e.stderr, e.stdout)

    finally:
        server.stop(0)


def test_separate_ca() -> None:
    address = random_address()
    print("Using address %s" % address, file=sys.stderr)
    cacert, cakey = pskca.create_certificate_and_key(ca=True)
    servercsr, serverkey = pskca.create_certificate_signing_request(
        cn="server",
    )
    servercert = pskca.issue_certificate(servercsr, cacert, cakey, ca=True)

    ca = pskca.CA(servercert, serverkey, [cacert, servercert])
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cakes_pb2_grpc.add_CAKESServicer_to_server(
        cakes.CAKESServicer(
            ca,
            cakes.unconditional_accept_ecdh,
            cakes.unconditional_accept_cert,
        ),
        server,
    )
    server.add_insecure_port(address)
    server.start()

    try:
        clientcsr, unused_key = pskca.create_certificate_signing_request()
        with grpc.insecure_channel(address) as channel:
            client = cakes.CAKESClient(
                channel,
                clientcsr,
                cakes.unconditional_accept_ecdh,
                cakes.unconditional_accept_cert,
            )
            clientcert, chain = client.run()
            try:
                verify_cert(chain, clientcert)
            except subprocess.CalledProcessError as e:
                assert 0, (e.stderr, e.stdout)

    finally:
        server.stop(0)
