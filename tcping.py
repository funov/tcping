import argparse

from ping_process import run


def create_parser():
    description = "Usage\ntcping [options] <destination>"

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        'destination',
        help='dns name or ip address',
        type=str
    )
    parser.add_argument(
        '--port',
        '-p',
        help='tcp port',
        type=int,
        default=80
    )
    parser.add_argument(
        '--count',
        '-c',
        help='stop after <count> replies',
        type=int,
        default=None
    )
    parser.add_argument(
        '--interval',
        '-i',
        help='seconds between sending each packet',
        type=float,
        default=None
    )
    parser.add_argument(
        '--wait',
        '-w',
        help='seconds time to wait for response',
        type=float,
        default=5
    )

    return parser


def main():
    parser = create_parser()
    cmd_commands = parser.parse_args()

    try:
        run(
            cmd_commands.destination,
            cmd_commands.port,
            cmd_commands.count,
            cmd_commands.interval,
            cmd_commands.wait
        )
    except RuntimeError:
        print('Something went wrong, write to the developers...')


if __name__ == '__main__':
    main()
