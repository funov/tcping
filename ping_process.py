from network.icmp_echo_reply import ICMPEchoReply
from network.icmp_socket import ICMPSocket
from network.icmp_echo_request import ICMPEchoRequest
from utils.timer import Timer

from time import sleep


def run(
        destination: str,
        port: int,
        count: int,
        interval: float,
        wait: float
):
    print_start(destination)

    if count is None:
        seq = 1
        while True:
            try:
                icmp_reply, timer = ping(destination, port, wait)

                print_ping(
                    destination,
                    port,
                    seq,
                    icmp_reply.ttl,
                    timer.get_ms_str()
                )

                if interval is not None:
                    sleep(interval)

                seq += 1
            except KeyboardInterrupt:
                print_statistics()
                break
    else:
        pass


def ping(destination: str, port: int, wait: float) -> (ICMPEchoReply, Timer):
    timer = Timer()
    timer.start()
    socket = ICMPSocket(wait)
    icmp_reply = ICMPEchoReply(
        socket.send_to(ICMPEchoRequest(), destination, port)
    )
    timer.stop()
    socket.close()

    return icmp_reply, timer


def print_start(host: str):
    print(f'PING {host} 48 bytes of data')


def print_ping(host: str, port: int, seq: int, ttl: int, ms: str):
    print(f'Connected to {host}[:{port}]: seq={seq} ttl={ttl} time={ms}')


def print_statistics():
    print(f'Statistics')
