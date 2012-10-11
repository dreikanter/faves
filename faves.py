#!/usr/bin/env python

import codecs
from datetime import datetime
import json
import requests
import time


lastfm_key = '1f4891f6fd8ecabbefd751deba2c95b7'  # It's a test key from API docs
lastfm_user = 'dreikanter'
api_url = 'http://ws.audioscrobbler.com/2.0/?'
dump_file = 'faves.json'


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
                print(str(e))

        if page >= int(data['lovedtracks']['@attr']['totalPages']):
            break

        page += 1

    return result


faves = get_faves(lastfm_user, lastfm_key)

with codecs.open(dump_file, mode='w', encoding='utf-8') as f:
    f.write(json.dumps(faves, indent=4, encoding='utf-8', ensure_ascii=False))

print("%d faves saved to '%s'" % (len(faves), dump_file))
