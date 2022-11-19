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
    if count is None:
        while True:
            try:
                timer = Timer()

                timer.start()

                socket = ICMPSocket(wait)
                socket.send_to(ICMPEchoRequest(), destination, port)

                timer.stop()

                print(timer.get_ms_str())

                if interval is not None:
                    sleep(interval)
            except KeyboardInterrupt:
                break
    else:
        pass
