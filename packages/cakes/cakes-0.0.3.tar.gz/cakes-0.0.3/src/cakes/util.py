from typing import List
import blindecdh
from cryptography.x509 import Certificate


def unconditional_accept_ecdh(
    peer: str,
    unused: blindecdh.CompletedECDH,
) -> bool:
    """
    Stub callback function to auto-accept an ECDH exchange.

    Do not use in production.  Blindly "verifying" an ECDH exchange without
    comparing the two CompleteECDH exchanges on both sides makes your code
    vulnerable to active man-in-the-middle attacks.
    """
    return True


def unconditional_accept_cert(
    peer: str,
    unused: Certificate,
    unused_list: List[Certificate],
) -> bool:
    """
    Stub callback function to auto-accept an issued certificate.

    You may use this in production.
    """
    return True
