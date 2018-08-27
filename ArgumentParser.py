import argparse

parser = argparse.ArgumentParser(
    description=
        'Service intended for running on RaspberryPi to switch lights via HomeHUD web interface.\n' +
        'Uses RabbitMQ queue to receive messages with light switch details.')

parser.add_argument(
    '--debuggingOnPC',
    action='store_true',
    help='using GPIO library reqiures running on Pi, add this flag when debugging on PC')

args = parser.parse_args()
debuggingOnPC = args.debuggingOnPC