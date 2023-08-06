import csv
import os.path

import numpy as np
import pyaaware
import yaml


def get_nnpdetect(channels: int, classes: int) -> pyaaware.NNPDetect:
    config = {
        'channels':   None,
        'classes':    None,
        'risethresh': None,
        'fallthresh': None,
        'riseframes': None,
        'fallframes': None,
        'hold':       None,
        'smoothf':    None,
    }

    if os.path.exists('.nnpdetect'):
        with open(file='.nnpdetect', mode='r') as f:
            config.update(yaml.safe_load(f))

    config['channels'] = channels
    config['classes'] = classes

    return pyaaware.NNPDetect(**config)


def _unpack_prob_entry(entry: int) -> (int, int, int):
    """Decode the packed probability data: [ 16-bit label | 8-bit zone | 8-bit probability ]."""
    data = np.array(entry, dtype=np.uint32)
    label = int(np.right_shift(data, 16))
    zone = int(np.bitwise_and(np.right_shift(data, 8), 0xFF))
    value = int(np.bitwise_and(entry, 0xFF))
    return zone, label, value


def parse_payload(payload: list) -> np.ndarray:
    """Parse MQTT probability payload from aawscd.

     Return a numpy array ([zones, labels])."""
    zones = set()
    labels = set()
    prob_list = list()

    for entry in payload:
        zone, label, value = _unpack_prob_entry(entry)
        zones.add(zone)
        labels.add(label)
        prob_list.append((zone, label, value))

    zones = list(zones)
    labels = list(labels)
    prob = np.zeros((len(zones), len(labels)), dtype=np.uint8)

    for entry in prob_list:
        zone, label, value = entry
        prob[zone, label] = value

    return prob


def get_zone_names(num_zones: int) -> list:
    """Return zone names in a list."""
    return [f'Zone {idx}' for idx in range(num_zones)]


def get_label_names(num_labels: int, file: str = None) -> list:
    """Return label names in a list. Read from CSV file, if provided."""
    if file is None:
        return [f'Class {val + 1}' for val in range(num_labels)]

    label_names = [''] * num_labels
    with open(file) as f:
        reader = csv.DictReader(f)
        if 'index' not in reader.fieldnames or 'display_name' not in reader.fieldnames:
            raise Exception(f'Missing required fields in labels CSV.')

        for row in reader:
            index = int(row['index']) - 1
            if index >= num_labels:
                raise Exception(f'The number of given label names does not match the number of labels.')
            label_names[index] = row['display_name']

    return label_names
