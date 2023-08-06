"""aawscd_probwrite

usage: aawscd_probwrite [-h] [-m MACHINE] [-f FRAMES] FILE

options:
   -h, --help
   -m MACHINE, --machine MACHINE    IP address of aawscd platform. [default: localhost].
   -f FRAMES, --frames FRAMES       Number of frames to capture. [default: 10].

aawscd_probwrite connects to an Aaware platform running aawscd and writes the sound classification
probability output to an HDF5 file.

"""
import signal
from threading import Condition

import h5py
import numpy as np
import paho.mqtt.client as mqtt
import yaml
from docopt import docopt
from tqdm import tqdm

import aawscd
from aawscd.tools import parse_payload

CLIENT = 'aawscd_probwrite'
TOPIC = 'aawscd/sc/prob'
DONE = Condition()
FRAMES = 10
FRAME_COUNT = 0
DATA = None
PROGRESS = None


def shutdown(_signum, _frame):
    global DONE
    with DONE:
        DONE.notify()


def on_message(_client, _userdata, message):
    global TOPIC
    if mqtt.topic_matches_sub(TOPIC, message.topic):
        payload = yaml.safe_load(str(message.payload.decode('utf-8')))
        prob = parse_payload(payload['prob'])

        global DATA
        global FRAMES
        if DATA is None:
            DATA = np.zeros((FRAMES, prob.shape[0], prob.shape[1]), dtype=prob.dtype)

        global FRAME_COUNT
        DATA[FRAME_COUNT] = prob
        FRAME_COUNT += 1

        global PROGRESS
        PROGRESS.update()

        if FRAME_COUNT == FRAMES:
            global DONE
            with DONE:
                DONE.notify()


def main():
    args = docopt(__doc__, version=aawscd.__version__, options_first=True)

    machine = args['--machine']

    global FRAMES
    FRAMES = int(args['--frames'])

    file = args['FILE']

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    global CLIENT
    client = mqtt.Client(client_id=CLIENT)
    client.on_message = on_message
    client.connect(host=machine)
    client.loop_start()
    global TOPIC
    client.subscribe(topic=TOPIC)

    global PROGRESS
    PROGRESS = tqdm(total=FRAMES, desc=file)

    with DONE:
        DONE.wait()

    PROGRESS.close()

    client.unsubscribe(topic=TOPIC)
    client.loop_stop()
    client.disconnect()

    global DATA
    with h5py.File(file, 'w') as f:
        f.create_dataset(name='prob', data=DATA)

    print(f'Wrote {file}')


if __name__ == '__main__':
    main()
