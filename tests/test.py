import io
import unittest.mock

from network.icmp_echo_reply import ICMPEchoReply
from network.icmp_echo_request import ICMPEchoRequest
from utils.printer import Printer


class PrinterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.host = '127.0.0.1'
        self.times = [1.1, 2.1, 3.1, None]
        self.times_none = [None, None, None]

        self.expected_result = '''
--- 127.0.0.1 ping statistics---
4 packets transmitted, 3 received, 25% packet loss, time 6.3 ms
rtt min/avg/max = 1.1/2.1/3.1 ms
'''
        self.expected_result_all_none = '''
--- 127.0.0.1 ping statistics---
3 packets transmitted, 0 received, 100% packet loss
'''

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_statistics(self, mock_stdout):
        Printer.print_statistics(self.host, self.times)
        self.assertEqual(mock_stdout.getvalue(), self.expected_result)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_statistics_all_none(self, mock_stdout):
        Printer.print_statistics(self.host, self.times_none)
        self.assertEqual(
            mock_stdout.getvalue(),
            self.expected_result_all_none
        )


class ICMPRequestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.bytes = b"\x08\x00\xfe\xf2\x89\x00\x01\x00" \
                     b"\xa5\x39\x0b\x00\x00\x00\x00\x00"

        self.expected_checksum = 48850

    def test_checksum(self):
        checksum = ICMPEchoRequest.get_checksum(self.bytes)
        self.assertEqual(self.expected_checksum, checksum)


class ICMPReplyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.bytes = b"\x45\x40\x00\x4c\x00\x00\x00\x00\x37\x01\x0a\xdf" \
            b"\x8e\xfa\x96\x5b\xac\x1d\xa7\x1f\x00\x00\x06\xf3" \
            b"\x89\x00\x01\x00\xa5\x39\x0b\x00\x00\x00\x00\x00" \
            b"\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b" \
            b"\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27" \
            b"\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33" \
            b"\x34\x35\x36\x37"
        self.ttl = 55
        self.type = 0
        self.code = 0

    def test_ttl(self):
        reply = ICMPEchoReply((self.bytes, ('127.0.0.1', 80)))
        self.assertEqual(self.ttl, reply.ttl)

    def test_code(self):
        reply = ICMPEchoReply((self.bytes, ('127.0.0.1', 80)))
        self.assertEqual(self.type, reply.type)

    def test_type(self):
        reply = ICMPEchoReply((self.bytes, ('127.0.0.1', 80)))
        self.assertEqual(self.code, reply.code)
