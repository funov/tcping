import io
import unittest
from socket import AddressFamily, SocketKind
from unittest import mock
from time import sleep

from network.icmp_echo_reply import ICMPEchoReply
from network.icmp_echo_request import ICMPEchoRequest
from network.icmp_socket import ICMPSocket
from utils.printer import Printer
from utils.timer import Timer


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

        self.custom_id = 2932
        self.expected_default_bytes_request = b'\x08\x00\x13\xe8t' \
            b'\x0b\x01\x00\xa59\x0b\x00\x00\x00' \
            b'\x00\x00\x10\x11\x12\x13\x14\x15' \
            b'\x16\x17\x18\x19\x1a\x1b\x1c\x1d' \
            b'\x1e\x1f !"#$%&\'()*+,-./01234567'

        self.custom_data = b"\xa5\x39\x0b\x00\x00\x00\x00\x00" \
            b"\x10\x11\x12\x13\x14\x15\x16\x17" \
            b"\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f" \
            b"\x20\x21\x22\x23\x24\x60\x26\x27" \
            b"\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f" \
            b"\x30\x31\x32\x33\x34\x35\x36\x37"
        self.expected_custom_bytes_request = b'\x08\x00\x13\xadt\x0b\x01' \
            b'\x00\xa59\x0b\x00\x00\x00\x00\x00\x10\x11\x12\x13' \
            b'\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f ' \
            b'!"#$`&\'()*+,-./01234567'

        self.expected_checksum = 48850

    def test_checksum(self):
        checksum = ICMPEchoRequest.get_checksum(self.bytes)
        self.assertEqual(self.expected_checksum, checksum)

    def test_default_bytes_request(self):
        request = ICMPEchoRequest(custom_id=self.custom_id)
        bytes_request = bytes(request)

        self.assertEqual(self.expected_default_bytes_request, bytes_request)

    def test_custom_bytes_request(self):
        request = ICMPEchoRequest(
            data=self.custom_data,
            custom_id=self.custom_id
        )
        bytes_request = bytes(request)

        self.assertEqual(self.expected_custom_bytes_request, bytes_request)


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


class TimerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.timer = Timer()

    def test_get_ms(self):
        self.timer.start()
        sleep(1)
        self.timer.stop()

        self.assertTrue(950 < self.timer.get_ms() < 1050)

    def test_get_ms_str(self):
        self.timer.start()
        sleep(1)
        self.timer.stop()

        ms = self.timer.get_ms()

        self.assertEqual(
            f'{round(ms, 1)} ms',
            self.timer.get_ms_str()
        )

    def test_get_ms_error(self):
        self.assertRaises(ValueError, self.timer.get_ms)


class ICMPSocketTests(unittest.TestCase):
    def setUp(self) -> None:
        self.request = ICMPEchoRequest()

        self.expected_socket_inf = (
            AddressFamily.AF_INET,
            SocketKind.SOCK_RAW,
            1
        )

        self.expected_port = 80
        self.expected_host = '127.0.0.1'
        self.expected_recv_size = (4096,)
        self.expected_reply = b'123'

        self.expected_timeout = (10,)

    def test_icmp_socket_without_timeout(self):
        with mock.patch('socket.socket') as mock_socket:
            mock_socket.return_value.recvfrom.return_value \
                = self.expected_reply
            icmp_socket = ICMPSocket()
            reply = icmp_socket.send_to(ICMPEchoRequest(), '127.0.0.1', 80)
            icmp_socket.close()

        self.assertEqual('', mock_socket.mock_calls[0][0])
        self.assertEqual(
            self.expected_socket_inf,
            mock_socket.mock_calls[0][1]
        )

        self.assertEqual('().settimeout', mock_socket.mock_calls[1][0])
        self.assertEqual((None,), mock_socket.mock_calls[1][1])

        self.assertEqual('().sendto', mock_socket.mock_calls[2][0])
        self.assertTrue(type(mock_socket.mock_calls[2][1][0]) is bytes)
        self.assertEqual(
            (self.expected_host, self.expected_port),
            mock_socket.mock_calls[2][1][1]
        )

        self.assertEqual('().recvfrom', mock_socket.mock_calls[3][0])
        self.assertEqual(
            self.expected_recv_size,
            mock_socket.mock_calls[3][1]
        )

        self.assertEqual('().close', mock_socket.mock_calls[4][0])

        self.assertEqual(self.expected_reply, reply)

    def test_icmp_socket_with_timeout(self):
        with mock.patch('socket.socket') as mock_socket:
            mock_socket.return_value.recvfrom.return_value \
                = self.expected_reply
            icmp_socket = ICMPSocket(10)
            icmp_socket.send_to(ICMPEchoRequest(), '127.0.0.1', 80)
            icmp_socket.close()

        self.assertEqual('().settimeout', mock_socket.mock_calls[1][0])
        self.assertEqual(self.expected_timeout, mock_socket.mock_calls[1][1])
