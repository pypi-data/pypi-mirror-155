# Certificate authority kit, ECDH-powered, SAS-authenticated

This package contains a kit that allows you to develop clients and servers
that authenticate to each other mutually, issuing certificates to clients that
can then be used for secure mutual TLS or gRPC authenticated communication.

You will find this package useful if:

* You have a server program, and a client program.
* You want to secure communications between these programs using SSL
  or gRPC secure channels.
* You do not have a certificate authority or other PKI system on hand.
* All you need is a way to authenticate the client on the server side,
  and the server on the client side.
* You want to authenticate the two parts by making a visual comparison
  on both sides (much like Bluetooth PIN pairing).


You'll find more developer and implementation documentation in the
[module](src/cakes/__init__.py).

This package is distributed under the GNU Lesser General Public License v2.1.
For relicensing, contact the package author.
