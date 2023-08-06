"""aawscd_wwrecord

usage: aawscd_wwrecord [-h] [-m MACHINE] [-d DURATION]

options:
   -h, --help
   -m MACHINE, --machine MACHINE        IP address of aawscd platform. [default: localhost].
   -d DURATION, --duration DURATION     Length of each recording. [default: 3].

aawscd_wwrecord connects to an Aaware platform running aawscd. When a detection occurs, it records
DURATION seconds of audio.

"""
import datetime
import signal
import subprocess
import time

import paho.mqtt.client as mqtt
import yaml
from docopt import docopt

import aawscd

CLIENT = 'aawscd_wwrecord'
TOPIC = 'aawscd/detect'
RUNNING = True


def shutdown(_signum, _frame):
    global RUNNING
    RUNNING = False


def on_message(_client, duration, message):
    if mqtt.topic_matches_sub(TOPIC, message.topic):
        msg = yaml.safe_load(str(message.payload.decode('utf-8')))
        now = datetime.datetime.now()
        filename = f'audio_{now.strftime("%Y%m%d%H%M%S")}_z{msg["azimuth"]}.wav'
        print('Capturing audio to ' + filename)
        dur = f'-d{duration}'
        _rsp = subprocess.Popen(['arecord', '-q', dur, '-r16000', '-fS32_LE', '-c1', filename],
                                stdout=subprocess.PIPE).communicate()[0]


def main():
    args = docopt(__doc__, version=aawscd.__version__, options_first=True)

    machine = args['--machine']
    duration = int(args['--duration'])

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    client = mqtt.Client(CLIENT, duration)
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
