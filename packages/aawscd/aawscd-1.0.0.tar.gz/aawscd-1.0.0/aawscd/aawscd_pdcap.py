"""aawscd_pdcap

usage: aawscd_pdcap [-h] [-m MACHINE] (-z ZONE) (-l LABEL)

options:
   -h, --help
   -m MACHINE, --machine MACHINE    IP address of aawscd platform. [default: localhost].
   -z ZONE, --zone ZONE             Zone index.
   -l LABEL, --label LABEL          Label index.

aawscd_pdcap connects to an Aaware platform running aawscd and issues a pdcap for the given zone and label.

"""
import signal
import time

import paho.mqtt.client as mqtt
import yaml
from docopt import docopt

import aawscd

CLIENT = 'aawscd_pdcap'
TOPIC = 'aawscd/pdcap/capture'
RUNNING = True


def shutdown(_signum, _frame):
    global RUNNING
    RUNNING = False


def on_message(_client, _userdata, message):
    if mqtt.topic_matches_sub(TOPIC, message.topic):
        payload = yaml.safe_load(str(message.payload.decode("utf-8")))
        print(f'Capturing zone {payload["zone"]}, phrase {payload["phrase"]}')
        global RUNNING
        RUNNING = False


def main() -> None:
    args = docopt(__doc__, version=aawscd.__version__, options_first=True)

    machine = args['--machine']
    zone = int(args['--zone'])
    label = int(args['--label'])

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    client = mqtt.Client(CLIENT)
    client.on_message = on_message
    client.connect(machine)
    client.loop_start()
    client.subscribe(TOPIC)
    client.publish('aawscd/pdcap/command/capture', f'zone: {zone}\nphrase: {label}')

    while RUNNING:
        time.sleep(0.2)

    client.unsubscribe(TOPIC)
    client.loop_stop()
    client.disconnect()


if __name__ == '__main__':
    main()
