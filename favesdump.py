#!/usr/bin/env python

from argparse import ArgumentParser
import codecs
from datetime import datetime
import json
import logging
import os
import requests
import time

__version__ = '0.0.2'

LOG_CONSOLE_FMT = ("%(asctime)s %(levelname)s: %(message)s", "%H:%M:%S")
LOG_FILE_FMT = ("%(asctime)s %(levelname)s: %(message)s", "%Y/%m/%d %H:%M:%S")
LASTFM_API_URL = 'http://ws.audioscrobbler.com/2.0/?'

log = None
conf = None


def init():
    """Script initialization"""

    args = get_args()

    global conf
    conf = {
        'lastfm_user': args.lastfm_user,
        'lastfm_key': args.key,
        'path': args.path,
        'format': args.format.lower(),
    }

    global log
    log = get_logger(args.log, args.verbose)


def get_args():
    """Command line parsing"""

    d = 'last.fm faves dumper, v' + __version__
    e = 'Have fun!'
    parser = ArgumentParser(description=d, epilog=e)

    parser.add_argument('lastfm_user',
                        metavar='USER',
                        help='last.fm user name')

    parser.add_argument('-p', '--path',
                        metavar='PATH',
                        default='{timestamp}_{user}.{format}',
                        help='downloads directory path')

    parser.add_argument('-k', '--key',
                        metavar='KEY',
                        default='1f4891f6fd8ecabbefd751deba2c95b7',
                        help='last.fm api key')

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='verbose logging')

    parser.add_argument('-l', '--log',
                        metavar='LOG',
                        help='log to file')

    parser.add_argument('-f', '--format',
                        choices=['yaml', 'json'],
                        default='json',
                        help='data format (default is \'json\')')

    return parser.parse_args()


def get_logger(log_file=None, verbose=False):
    """Logging initialization"""

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


def req(url, **kwargs):
    get_params = ["%s=%s" % (k, v) for k, v in kwargs.items()]
    r = requests.get(url + '&'.join(get_params))
    return json.loads(r.text)


def get_faves(user, key):
    page = 1
    result = []
    while True:
        data = req(LASTFM_API_URL,
                   method='user.getlovedtracks',
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


def dump_file():
    file_name = conf['path']
    replacements = {
        '{timestamp}': datetime.now().strftime("%Y%m%d"),
        '{user}': conf['lastfm_user'],
        '{format}': conf['format'],
    }

    for k, v in replacements.items():
        file_name = file_name.replace(k, v)

    return file_name


def main():
    init()
    faves = get_faves(conf['lastfm_user'], conf['lastfm_key'])
    makedirs(os.path.dirname(dump_file()))
    with codecs.open(dump_file(), mode='w', encoding='utf-8') as f:
        if conf['format'] == 'json':
            result = json.dumps(faves, indent=4, ensure_ascii=False)
        else:
            import yaml
            result = yaml.dump(faves, width=79, indent=2, allow_unicode=True,
                               default_flow_style=False)
        f.write(result)
        log.info("%d %s's faves saved to '%s'" % \
                 (len(faves), conf['lastfm_user'], dump_file()))


if __name__ == '__main__':
    main()
