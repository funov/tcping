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
        times = []
        while True:
            try:
                icmp_reply, timer = ping(destination, port, wait)

                if len(icmp_reply.bytes_reply) != 0:
                    times.append(timer.get_ms())

                    print_ping(
                        destination,
                        port,
                        seq,
                        icmp_reply.ttl,
                        timer.get_ms_str()
                    )
                else:
                    print('WRONG')

                if interval is not None:
                    sleep(interval)

                seq += 1
            except KeyboardInterrupt:
                print_statistics(destination, times)
                break
    else:
        for i in range(count):
            print(i)


def ping(destination: str, port: int, wait: float) -> (ICMPEchoReply, Timer):
    timer = Timer()
    timer.start()
    socket = ICMPSocket(wait)
    reply = socket.send_to(ICMPEchoRequest(), destination, port)
    icmp_reply = ICMPEchoReply(reply)
    timer.stop()
    socket.close()

    return icmp_reply, timer


def print_start(host: str):
    print(f'PING {host} 48 bytes of data')


def print_ping(host: str, port: int, seq: int, ttl: int, ms: str):
    print(f'Connected to {host}[:{port}]: seq={seq} ttl={ttl} time={ms}')


def print_statistics(host: str, times: list):
    n = len(times)

    print(f'\n--- {host} ping statistics---')
    print(f'{n} packets transmitted, time {sum(times)} ms')
    print(f'rtt min/avg/max = {min(times)}/{sum(times) / n}/{max(times)} ms')
