import requests
from json import loads

URL = "https://chorus.fightthe.pw/api/search"


def search_by_artist(artist):
    count = 0
    results = []
    while True:
        payload = {'query': f'artist="{artist}"', 'from': count}
        res = requests.get(URL, params=payload)
        if (res.status_code != 200):
            raise Exception("Request failed")
            break
        songs = loads(res.text)['songs']
        if (len(songs) == 0):
            break
        for song in songs:
            results.append(song)
        count += 20
    return results
