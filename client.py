import time
from threading import Thread
from typing import Any, Dict

import requests
import random

import lamp
from lamp import Console

try:
    from secrets import secrets
except ImportError:
    print('Secrets are kept in secrets.py, please add them there!')
    raise

#aio_api = secrets['aio_api']
#aio_key = secrets['aio_key']

def aio_api():
    return secrets['aio_api']

def aio_key():
    return secrets['aio_key']

def construct_call(value: Any = None) -> Dict[str, Any]:
    data = {'X-AIO-Key': aio_key()}
    if value is not None:
        data['value'] = value
    return data

def check_color(my_lamp: Console) -> None:
    api_response = requests.get(aio_api(), data = construct_call()).json()
    current_color = api_response[0]['value']
    current_color = lamp.rgb_decode(int(current_color))
    if current_color != my_lamp.get_color():
        my_lamp.set_color(current_color)
    return None


def trigger_color_change(my_lamp: Console) -> None:
    new_color = lamp.suggest_rgb(my_lamp.get_color())
    my_lamp.set_color(new_color)
    post_data = construct_call(lamp.rgb_encode(new_color))
    api_response = requests.post(aio_api(), data = post_data)
    print(f'New color: {new_color}, response: {api_response.json()}')
    return None


def main():
    magic_lamp = Console()
    check_color(magic_lamp)

    while True:
        if random.random() >= .5:
            print('Changing color')
            trigger_color_change(magic_lamp)
        thread = Thread(target = check_color(magic_lamp))
        thread.start()
        
        time.sleep(5)




if __name__ == '__main__':
    main()
