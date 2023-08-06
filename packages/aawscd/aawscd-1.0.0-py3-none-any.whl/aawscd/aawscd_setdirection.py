"""aawscd_setdirection

usage: aawscd_setdirection [-h] [-m MACHINE] ZONE

options:
   -h, --help
   -m MACHINE, --machine MACHINE    IP address of aawscd platform. [default: localhost].

aawscd_setdirection connects to an Aaware platform running aawscd and sets the streaming output's
direction to ZONE.

"""
import signal
import time

import paho.mqtt.client as mqtt
import yaml
from docopt import docopt

import aawscd

CLIENT = 'aawscd_setdirection'
TOPIC = 'aawscd/strmout/set_zone'
RUNNING = True


def shutdown(_signum, _frame):
    global RUNNING
    RUNNING = False


def on_message(_client, _userdata, message):
    if mqtt.topic_matches_sub(TOPIC, message.topic):
        payload = yaml.safe_load(str(message.payload.decode("utf-8")))
        print(f'Set streaming output direction to {payload["zone"]}')
        global RUNNING
        RUNNING = False


def main() -> None:
    args = docopt(__doc__, version=aawscd.__version__, options_first=True)

    machine = args['--machine']
    zone = int(args['ZONE'])

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    client = mqtt.Client(CLIENT)
    client.on_message = on_message
    client.connect(machine)
    client.loop_start()
    client.subscribe(TOPIC)
    client.publish('aawscd/strmout/command/set_zone', f'zone: {zone}')

    while RUNNING:
        time.sleep(0.1)

    client.unsubscribe(TOPIC)
    client.loop_stop()
    client.disconnect()


if __name__ == '__main__':
    main()
