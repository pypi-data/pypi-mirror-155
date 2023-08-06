"""aawscd_getconf

usage: aawscd_getconf [-h] [-m MACHINE]

options:
   -h, --help
   -m MACHINE, --machine MACHINE    IP address of aawscd platform. [default: localhost].

aawscd_getconf connects to an Aaware platform running aawscd and displays the configuration.

"""
import signal
import time

import paho.mqtt.client as mqtt
import yaml
from docopt import docopt

import aawscd

CLIENT = 'aawscd_getconf'
TOPIC = 'aawscd/config'
RUNNING = True


def shutdown(_signum, _frame):
    global RUNNING
    RUNNING = False


def on_message(_client, _userdata, message):
    if mqtt.topic_matches_sub(TOPIC, message.topic):
        payload = yaml.safe_load(str(message.payload.decode('utf-8')))
        print(payload['config'])
        global RUNNING
        RUNNING = False


def main():
    args = docopt(__doc__, version=aawscd.__version__, options_first=True)

    machine = args['--machine']

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    client = mqtt.Client(CLIENT)
    client.on_message = on_message
    client.connect(machine)
    client.loop_start()
    client.subscribe(TOPIC)
    client.publish('aawscd/command/config')

    while RUNNING:
        time.sleep(0.2)

    client.unsubscribe(TOPIC)
    client.disconnect()
    client.loop_stop()


if __name__ == '__main__':
    main()
