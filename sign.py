#!/usr/bin/env python3

import time
from random import choice
from requests import Session

class PanicSignException(Exception):
    pass

class PanicSignTooManyRequest(PanicSignException):

    def __init__(self):
        super(PanicSignTooManyRequest, self).__init__('Too Many Requests')

class PanicSign(object):
    BASE = 'https://signserver.panic.com'

    COLORS = [
        'red',
        'orange',
        'yellow',
        'green',
        'green2',
        'teal',
        'lightblue',
        'blue',
        'purple',
        'pink'
    ]

    def __init__(self):
        sess = Session()
        sess.headers.update({'X-RateLimit-Limit': '1000'})
        sess.headers.update({'X-RateLimit-Remaining': '1000'})
        self._sess = sess

    def _request(self, method, path, params=None, data=None):
        url = '{}{}'.format(self.BASE, path)
        resp = self._sess.request(method, url, params=params, json=data)
        if resp.status_code == 429:
            raise PanicSignTooManyRequest()
        resp.raise_for_status()
        return resp

    def get_current_colors(self):
        path = '/get/string'
        return self._request('GET', path).json()

        '''
        Response:
        {
            "topColor": "blue",
            "bottomColor":"green2"
        }
        '''

    def set_colors(self, color1, color2):
        if color1 in self.COLORS and color2 in self.COLORS:
            path = '/set/{}/{}'.format(color1, color2)
            if self._request('GET', path).status_code == 200:
                '''Response returns text: "Done", make a JSON response instead'''
                return '{ "status": "success", "message": "colors changed" }'
        else:
            return '{ "status": "unsuccessful", "message": "color choice(s) not valid" }'



def rainbow():
    print('Running rainbow sequence...')
    panic = PanicSign()
    for color in panic.COLORS:
        print('Top: {}, Bottom: {}'.format(color, color))
        panic.set_colors(color, color)
        time.sleep(10)

def rainbow_alt():
    print('Running rainbow alternating sequence...')
    panic = PanicSign()
    for i in range(len(panic.COLORS)):
        color1 = panic.COLORS[i]
        try:
            color2 = panic.COLORS[i+1]
        except IndexError:
            color2 = panic.COLORS[0]

        print('Top: {}, Bottom: {}'.format(color1, color2))
        panic.set_colors(color1, color2)
        time.sleep(10)

def random():
    print('Running random color sequence...')
    panic = PanicSign()
    color1 = choice(panic.COLORS)
    color2 = choice(panic.COLORS)
    print('Top: {}, Bottom: {}'.format(color1, color2))
    panic.set_colors(color1, color2)

#rainbow()
#rainbow_alt()
random()
