"""aawscd_probmon

usage: aawscd_probmon [-hs] [-m MACHINE] [-n NUM] [-l LABELS]

options:
   -h, --help
   -m MACHINE, --machine MACHINE    IP address of aawscd platform. [default: localhost].
   -n NUM, --num NUM                Maximum number of labels to display. [default: 0].
   -l LABELS, --labels LABELS       CSV file containing index, display_name for labels.
   -s, --smooth                     Display smoothed probability.

aawscd_probmon connects to an Aaware platform running aawscd and displays the highest value labels
from the sound classification probability output. If NUM is 0 (the default), then all labels are
displayed.

"""
import curses
import signal
from queue import Queue
from threading import Condition
from typing import Union

import numpy as np
import paho.mqtt.client as mqtt
import pyaaware
import yaml
from docopt import docopt

import aawscd
import aawscd.tools

CLIENT = 'aawscd_probmon'
TOPIC = 'aawscd/sc/prob'
DONE = False
CONDITION = Condition()
PROB_QUEUE = Queue()
LABEL_FILE = None
LABEL_NAMES = list()
ZONE_NAMES = list()
USE_SMOOTH = False
NUM = 0
NNPDETECT: Union[pyaaware.NNPDetect, None] = None


def shutdown(_signum, _frame):
    global CONDITION
    with CONDITION:
        global DONE
        DONE = True

        CONDITION.notify()


def on_message(_client, _userdata, message):
    global TOPIC
    if mqtt.topic_matches_sub(TOPIC, message.topic):
        payload = yaml.safe_load(str(message.payload.decode('utf-8')))
        global CONDITION
        with CONDITION:
            prob = aawscd.tools.parse_payload(payload['prob'])

            global PROB_QUEUE
            PROB_QUEUE.put(prob)

            global NNPDETECT
            if NNPDETECT is None:
                NNPDETECT = aawscd.tools.get_nnpdetect(channels=prob.shape[0], classes=prob.shape[1])

                global LABEL_FILE
                global LABEL_NAMES
                LABEL_NAMES = aawscd.tools.get_label_names(num_labels=prob.shape[1], file=LABEL_FILE)

                global ZONE_NAMES
                ZONE_NAMES = aawscd.tools.get_zone_names(num_zones=prob.shape[0])

            CONDITION.notify()


def update_screen(window, prob: np.ndarray) -> None:
    window.erase()

    global NNPDETECT
    detect = NNPDETECT.execute(np.single(prob) / 255, True)

    values = prob

    global USE_SMOOTH
    if USE_SMOOTH:
        values = np.uint8(NNPDETECT.smooth() * 255)

    # Eliminate columns (zones) that contain all zeros
    zone_idx = np.where(values.any(axis=1))[0]

    # Sort by the sum across columns (zones) in descending order
    label_idx = np.argsort(values.sum(axis=0))[::-1]

    # Only display the first 'num' rows (labels)
    # NOTE: Doing the row reduction here (after converting the data to string) ensures that the
    # column width for the display names is maintained for the longest display name.
    global NUM
    if NUM <= 0:
        num = len(values)
    else:
        num = min(len(values), NUM)
    label_idx = label_idx[0:num]

    values = values[zone_idx, :]
    detect = detect[zone_idx, :]
    zone_names = np.array(ZONE_NAMES)[zone_idx].tolist()

    max_zone_len = len(max(ZONE_NAMES, key=len))
    zone_names = [f'{z:{max_zone_len + 1}}' for z in zone_names]

    max_label_len = len(max(LABEL_NAMES, key=len))
    text = list()
    text.append(f'{" ":{max_label_len}} {" ".join(zone_names)}')
    for idx in label_idx:
        probs = [f'{p:{max_zone_len}}{"*" if detect[i, idx] == 1 else " "}' for i, p in enumerate(values[:, idx])]
        text.append(f'{LABEL_NAMES[idx]:{max_label_len}} {" ".join(probs)}')

    for idx, val in enumerate(text):
        window.addstr(idx, 0, val)

    window.refresh()


def main_window(window) -> None:
    window.clear()
    window.refresh()
    window.nodelay(True)
    curses.curs_set(0)

    while True:
        global CONDITION
        with CONDITION:
            CONDITION.wait()

            global DONE
            if DONE or window.getch() == ord('q'):
                break

            global PROB_QUEUE
            while not PROB_QUEUE.empty():
                update_screen(window, PROB_QUEUE.get())


def main():
    args = docopt(__doc__, version=aawscd.__version__, options_first=True)

    machine = args['--machine']

    global LABEL_FILE
    LABEL_FILE = args['--labels']

    global USE_SMOOTH
    USE_SMOOTH = args['--smooth']

    global NUM
    NUM = int(args['--num'])

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    client = mqtt.Client(client_id=CLIENT)
    client.on_message = on_message
    client.connect(host=machine)
    client.loop_start()
    client.subscribe(topic=TOPIC)

    curses.wrapper(main_window)

    client.unsubscribe(topic=TOPIC)
    client.loop_stop()
    client.disconnect()


if __name__ == '__main__':
    main()
