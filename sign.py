#!/usr/bin/env python3

import time, argparse
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

    MODES = [
        'rainbow',
        'rainbow_alt',
        'random'
    ]

    def __init__(self, timewait=10):
        sess = Session()
        sess.headers.update({'X-RateLimit-Limit': '1000'})
        sess.headers.update({'X-RateLimit-Remaining': '1000'})
        self._sess = sess
        self.timewait = timewait

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
            print('Top: {}, Bottom: {}'.format(color1, color2))
            path = '/set/{}/{}'.format(color1, color2)
            if self._request('GET', path).status_code == 200:
                '''Response returns text: "Done", make a JSON response instead'''
                return '{ "status": "success", "message": "colors changed" }'
        else:
            return '{ "status": "unsuccessful", "message": "color choice(s) not valid" }'

    def rainbow(self):
        for color in self.COLORS:
            self.set_colors(color, color)
            time.sleep(self.timewait)

    def rainbow_alt(self):
        print('Running rainbow alternating sequence...')
        for i in range(len(self.COLORS)):
            color1 = self.COLORS[i]
            try:
                color2 = self.COLORS[i+1]
            except IndexError:
                color2 = self.COLORS[0]

            self.set_colors(color1, color2)
            time.sleep(self.timewait)

    def random(self):
        print('Running random color sequence...')
        color1 = choice(self.COLORS)
        color2 = choice(self.COLORS)
        self.set_colors(color1, color2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Modify the Panic Sign')
    parser.add_argument('--top', choices=PanicSign.COLORS, help='Color to assign to top of sign')
    parser.add_argument('--bottom', choices=PanicSign.COLORS, help='Color to assign to bottom of sign')
    parser.add_argument('--mode', choices=PanicSign.MODES, help='Mode to run')
    parser.add_argument('--wait', help='Time to wait between changing colors')
    args = parser.parse_args()

    panic = PanicSign()
    if args.wait:
        panic = panic = PanicSign(args.wait)

    if args.top and args.bottom:
        panic.set_colors(args.top, args.bottom)

    if args.mode == 'rainbow':
        panic.rainbow()
    elif args.mode == 'rainbow_alt':
        panic.rainbow_alt()
    elif args.mode == 'random':
        panic.random()
