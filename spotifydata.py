from requests import Session, get, post
from random import randint
from json import dump, dumps, load, loads
from os import system as sy
from argparse import ArgumentParser

p = print
sy('cls')

s = Session()

parser = ArgumentParser()
parser.add_argument('-url', '--url', required=False)

def song_data(token, s, url, v, Bearer):
    operationName = 'getTrack'
    variables = '%7B%22uri%22%3A%22spotify%3Atrack%3A{}%22%7D'.format(url.replace('https://open.spotify.com/track/', ''))
    extensions = '%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22ae85b52abb74d20a4c331d4143d4772c95f34757bfa8c625474b912b9055b5c0%22%7D%7D'

    headers = {
    'authority': 'api-partner.spotify.com',
    'accept': 'application/json',
    'accept-language': 'en',
    'app-platform': 'WebPlayer',
    'authorization': 'Bearer {}'.format(Bearer),
    'cache-control': 'no-cache',
    'client-token': token,
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://open.spotify.com',
    'pragma': 'no-cache',
    'referer': 'https://open.spotify.com/',
    'sec-ch-ua': '"Chromium";v="{}", "Not(A:Brand";v="24", "Google Chrome";v="{}"'.format(v, v),
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'spotify-app-version': '1.2.33.0-unknown',
    'user-agent': 'Mozilla/5.0 (Windows NT {}.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{}.0.0.0 Safari/537.36'.format(randint(10, 11), v)
    }

    r = get("https://api-partner.spotify.com/pathfinder/v1/query?operationName={}&variables={}&extensions={}".format(operationName, variables, extensions), headers=headers, data={})

    if r.status_code == 200:
        r = r.json()
        streams = int(r.get('data').get('trackUnion').get('playcount'))

        return streams

    else:
        p(f'Failed To Get Clienttoken: {r.text}')

def album_data(token, s, url, v, Bearer):
    track_count = 0
    album_analytics = []
    total_album_streams = 0

    headers = {
    'authority': 'api-partner.spotify.com',
    'accept': 'application/json',
    'accept-language': 'en',
    'app-platform': 'WebPlayer',
    'authorization': 'Bearer {}'.format(Bearer),
    'cache-control': 'no-cache',
    'client-token': token,
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://open.spotify.com',
    'pragma': 'no-cache',
    'referer': 'https://open.spotify.com/',
    'sec-ch-ua': '"Chromium";v="{}", "Not(A:Brand";v="24", "Google Chrome";v="{}"'.format(v, v),
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'spotify-app-version': '1.2.33.0-unknown',
    'user-agent': 'Mozilla/5.0 (Windows NT {}.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{}.0.0.0 Safari/537.36'.format(randint(10, 11), v)
}
    
    uri = url.replace('https://open.spotify.com/album/', '')

    params = (
        ('operationName', 'getAlbum'),
        ('variables', '{{"uri":"spotify:album:{}","locale":"","offset":0,"limit":50}}'.format(uri)),
        ('extensions', '{"persistedQuery":{"version":1,"sha256Hash":"469874edcad37b7a379d4f22f0083a49ea3d6ae097916120d9bbe3e36ca79e9d"}}'),
    )

    r = get('https://api-partner.spotify.com/pathfinder/v1/query', headers=headers, params=params)

    if r.status_code == 200:
        r = r.json()
        album_tracks = r.get('data').get('albumUnion').get('tracks').get('items')
        for track in album_tracks:
            track_count+=1
            track_data = {
                'track_number': track_count,
                'track_name': track.get('track').get('name'),
                'primary_artist': track.get('track').get('artists').get('items')[0].get('profile').get('name'),
                'streams': int(track.get('track').get('playcount')),
                'streams_formatted': '{:,}'.format(int(track.get('track').get('playcount'))),
                'uid': track.get('uid'),
            }

            total_album_streams+=track_data.get('streams')
            album_analytics.append(track_data)

        total_album_streams = {
            'total_album_streams': '{:,}'.format(total_album_streams)
        }
        release_name = {
            'release_name': r.get('data').get('albumUnion').get('name')
        }

        album_analytics.append(release_name)   
        album_analytics.append(total_album_streams)   
     
        return album_analytics

    else:
        p(f'Failed To Get Clienttoken: {r.text}, {r.status_code}, {token}')

def song_data_(url, Bearer):
    payload = dumps({
    "client_data": {
        "client_version": "1.2.33.0-unknown",
        "client_id": "d8a5ed958d274c2e8ee717e6a4b0971d",
        "js_sdk_data": {
        "device_brand": "unknown",
        "device_model": "unknown",
        "os": "windows",
        "os_version": "NT 10.0",
        "device_id": "2d1c92cd52f9695eba99f6ae60d7f764",
        "device_type": "computer"
        }
    }
    })
    v = randint(15, 22)

    headers = {
    'authority': 'clienttoken.spotify.com',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://open.spotify.com',
    'pragma': 'no-cache',
    'referer': 'https://open.spotify.com/',
    'sec-ch-ua': '"Chromium";v="{}", "Not(A:Brand";v="24", "Google Chrome";v="{}"'.format(v, v),
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{}.0.0.0 Safari/537.36'.format(v, v)
    }

    r = s.post("https://clienttoken.spotify.com/v1/clienttoken", headers=headers, data=payload)
    if r.status_code == 200:
        r = r.json()
        token = r.get('granted_token').get('token')
    else:
        p(f'Failed To Get Clienttoken: {r.text}')
    
    if url:
        pass
    else:
        url = input('Song Link?: ')

    if url.startswith('https://open.spotify.com/track/'):
        if '?si=' in url:
            url = url.split('?si=')[0]
            streams = song_data(token, s, url, v, Bearer)
            if streams:
                return streams
            else:
                return 'Failed To Get Clienttoken: Token expired'

    elif url.startswith('https://open.spotify.com/album/'):
        album_analytics = album_data(token, s, url, v, Bearer)
        if album_analytics:
            return album_analytics
        else:
            return 'Failed To Get Clienttoken: Token expired'


if __name__ == "__main__":
    pass