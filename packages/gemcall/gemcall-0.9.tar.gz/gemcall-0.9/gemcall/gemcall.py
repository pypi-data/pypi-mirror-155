# vim: tabstop=4 shiftwidth=4 expandtab

import socket as sockets
import urllib.parse
import ssl

from Crypto.PublicKey import RSA, ECC

class Response():
    def __init__(self, socket: sockets.socket) -> "Response":
        self._socket = socket

        cert: bytes = self._socket.getpeercert(binary_form=True)
        try:
            certobj: RSA.RsaKey = RSA.import_key(cert)
        except ValueError:
            certobj: ECC.EccKey = ECC.import_key(cert)
        # "\n" is added for API compatibility
        pubkey: str = certobj.public_key().export_key(format="PEM") + "\n"

        self.serverpubkey: bytes = pubkey.encode()
        self._filehandle = self._socket.makefile(mode = "rb")

        # Two code digits, one space and a maximum of 1024 bytes of meta info.
        try:
            self.responsecode, self.meta = self._filehandle.readline(1027).split(maxsplit=1)
            self.responsecode = int(self.responsecode)
            self.meta = self.meta.strip().decode("UTF-8")
        except Exception as err:
            self.discard()
            raise RuntimeError("Received malformed header from gemini server") from err

    def read(self, bufsize: int = 4096) -> bytes:
        return self._filehandle.read(bufsize)

    def readline(self, bufsize: int = 4096) -> bytes:
        return self._filehandle.readline(bufsize)

    def discard(self) -> None:
        self._filehandle.close()
        self._socket.close()

def request(url: str = "", clientcert: str = None, clientkey: str = None, timeout: int = 3) -> Response:
    url: str = url if url.startswith("gemini://") else "gemini://" + url
    parsed = urllib.parse.urlparse(url)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    if (clientcert and clientkey):
        context.load_cert_chain(clientcert, clientkey)

    sock = sockets.create_connection((parsed.hostname, parsed.port or 1965))
    ssock = context.wrap_socket(sock, server_hostname=parsed.hostname)
    ssock.sendall((url+"\r\n").encode("UTF-8"))

    return Response(ssock)
