import struct


class ICMPEchoReply:
    def __init__(self, reply: bytes):
        self.bytes_reply = reply
        self.ttl = int(struct.unpack("B", reply[0][8:9])[0])
