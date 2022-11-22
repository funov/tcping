class Printer:
    @staticmethod
    def start(host: str):
        print(f'PING {host} 48 bytes of data')

    @staticmethod
    def print_success_ping(host: str, port: int, seq: int, ttl: int, ms: str):
        print(f'Connected to {host}[:{port}]: seq={seq} ttl={ttl} time={ms}')

    @staticmethod
    def print_unexpected_type(_type: int):
        print(f'Unexpected type={_type}, should have been 0')

    @staticmethod
    def print_unexpected_code(code: int):
        print(f'Unexpected type={code}, should have been 0')

    @staticmethod
    def print_timelimit():
        print(f"Reply didn't have time to come")

    @staticmethod
    def print_statistics(host: str, times: list):
        n = len(times)

        n_received = sum([0 if time is None else 1 for time in times])
        n_loss = n - n_received

        times = [0 if time is None else time for time in times]
        loss = int(n_loss / n * 100)
        total_time = round(sum(times), 1)
        min_times = round(min(times), 1)
        avg_times = round(sum(times) / n_received, 1)
        max_times = round(max(times), 1)

        print(f'\n--- {host} ping statistics---')
        print(f'{n} packets transmitted, {n_received} received, '
              f'{loss}% packet loss, time {total_time} ms')
        print(f'rtt min/avg/max = {min_times}/{avg_times}/{max_times} ms')
