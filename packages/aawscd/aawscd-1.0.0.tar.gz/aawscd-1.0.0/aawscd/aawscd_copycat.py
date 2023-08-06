"""aawscd_copycat

usage: aawscd_copycat [-h] [-m MACHINE]

options:
   -h, --help
   -m MACHINE, --machine MACHINE    IP address of aawscd platform. [default: localhost].

aawscd_copycat connects to an Aaware platform running aawscd. When a detection occurs, it records
three seconds of audio and then plays it back.

"""
import signal
import subprocess
import time

import paho.mqtt.client as mqtt
import yaml
from docopt import docopt

import aawscd

CLIENT = 'aawscd_copycat'
TOPIC = 'aawscd/detect'
RUNNING = True
FILENAME = 'output.wav'


def shutdown(_signum, _frame):
    global RUNNING
    RUNNING = False


def on_message(_client, _userdata, message):
    if mqtt.topic_matches_sub(TOPIC, message.topic):
        msg = yaml.safe_load(str(message.payload.decode('utf-8')))
        print('Detected ' + msg['phrase'] + ' in direction ' + repr(msg['azimuth']) + ' at ' + msg['time'])
        _rsp = subprocess.Popen(['arecord', '-q', '-d3', '-r16000', '-fS32_LE', '-c1', FILENAME],
                                stdout=subprocess.PIPE).communicate()[0]
        _rsp = subprocess.Popen(['play', '-q', FILENAME], stdout=subprocess.PIPE).communicate()[0]


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

    print('Listening for wake word')
    while RUNNING:
        time.sleep(0.2)

    client.unsubscribe(TOPIC)
    client.disconnect()
    client.loop_stop()


if __name__ == '__main__':
    main()
