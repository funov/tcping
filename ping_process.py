import socket

from network.icmp_echo_reply import ICMPEchoReply
from network.icmp_socket import ICMPSocket
from network.icmp_echo_request import ICMPEchoRequest
from utils.timer import Timer
from utils.printer import Printer

from time import sleep


def run(host: str, port: int, count: int, interval: float, wait: float):
    Printer.start(host)

    seq = 1
    times = []

    while True:
        try:
            time = ping(host, port, wait, interval, seq)
            times.append(time)

            if count == seq - 1:
                break

            seq += 1
        except KeyboardInterrupt:
            Printer.print_statistics(host, times)
            break

    Printer.print_statistics(host, times)


def ping(destination: str, port: int, wait: float, interval: float, seq: int):
    stat = _ping_with_errors_handling(destination, port, wait, seq)

    if interval is not None:
        sleep(interval)

    return stat


def _ping_with_errors_handling(destination: str, port: int, wait: float, seq: int):
    try:
        reply, timer = _ping(destination, port, wait)

        if reply.type != 0:
            Printer.print_unexpected_type(reply.type)
        elif reply.code != 0:
            Printer.print_unexpected_code(reply.code)
        else:
            Printer.print_success_ping(destination, port, seq, reply.ttl, timer.get_ms_str())

        return timer.get_ms()

    except socket.timeout:
        Printer.print_timelimit()

    return None


def _ping(destination: str, port: int, wait: float) -> (ICMPEchoReply, Timer):
    timer = Timer()
    timer.start()
    socket = ICMPSocket(wait)
    reply = socket.send_to(ICMPEchoRequest(), destination, port)
    icmp_reply = ICMPEchoReply(reply)
    timer.stop()
    socket.close()

    return icmp_reply, timer
