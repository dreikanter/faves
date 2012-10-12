#!/usr/bin/env python

import codecs
from datetime import datetime
import json
import logging
import os
import requests
import time

LOG_CONSOLE_FMT = ("%(asctime)s %(levelname)s: %(message)s", "%H:%M:%S")
LOG_FILE_FMT = ("%(asctime)s %(levelname)s: %(message)s", "%Y/%m/%d %H:%M:%S")

lastfm_key = '1f4891f6fd8ecabbefd751deba2c95b7'  # It's a test key from API docs
lastfm_user = 'dreikanter'
api_url = 'http://ws.audioscrobbler.com/2.0/?'
dump_file = 'faves.json'
log_file = '%s.log' % __name__


def get_logger(log_file=None, verbose=False):
    try:
        log = logging.getLogger(__name__)
        log.setLevel(logging.DEBUG)

        channel = logging.StreamHandler()
        channel.setLevel(logging.DEBUG if verbose else logging.INFO)
        fmt = logging.Formatter(LOG_CONSOLE_FMT[0], LOG_CONSOLE_FMT[1])
        channel.setFormatter(fmt)
        log.addHandler(channel)

        if log_file:
            makedirs(os.path.dirname(log_file))
            channel = logging.FileHandler(log_file)
            channel.setLevel(logging.DEBUG)
            fmt = logging.Formatter(LOG_FILE_FMT[0], LOG_FILE_FMT[1])
            channel.setFormatter(fmt)
            log.addHandler(channel)

        return log

    except:
        logging.error('logging initialization failed')
        raise


def makedirs(dir_path):
    """Creates directory if it not exists"""
    if dir_path and not os.path.exists(dir_path):
        log.debug("creating directory '%s'" % dir_path)
        os.makedirs(dir_path)


def req(**kwargs):
    get_params = ["%s=%s" % (k, v) for k, v in kwargs.iteritems()]
    url = api_url + '&'.join(get_params)
    r = requests.get(url)
    return json.loads(r.text)


def get_faves(user, key):
    page = 1
    result = []
    while True:
        data = req(method='user.getlovedtracks',
                   user=user,
                   api_key=key,
                   format='json',
                   page=page)

        for track in data['lovedtracks']['track']:
            try:
                date = time.strptime(track['date']['#text'], "%d %b %Y, %H:%M")
                date = time.mktime(date)
                date = datetime.fromtimestamp(date).strftime("%Y/%m/%d")
                result.append({
                    'artist': track['artist']['name'],
                    'date': date,
                    'name': track['name'],
                })
            except Exception as e:
                log.info(str(e))

        if page >= int(data['lovedtracks']['@attr']['totalPages']):
            break

        page += 1

    return result


log = get_logger(log_file, True)
faves = get_faves(lastfm_user, lastfm_key)

with codecs.open(dump_file, mode='w', encoding='utf-8') as f:
    f.write(json.dumps(faves, indent=4, encoding='utf-8', ensure_ascii=False))

log.info("%d faves saved to '%s'" % (len(faves), dump_file))
