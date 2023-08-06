from .api import search_by_artist
import json
from os import path, makedirs


def compare(names, mode, filepath, verbose, vars=[]):
    res = []
    for name in names:
        if verbose:
            print(f"Checking {name}")
        results = search_by_artist(name)
        count = len(results)
        if mode == 0:
            res.append(output_custom(name, results,
                       count, ['link']))
        elif mode == 1:
            res.append(output_songs(name, results, count))
        elif mode == 2:
            res.append(output_songs_raw(name, results, count))
        elif mode == 3:
            res.append(output_custom(name, results, count, vars))
        if verbose:
            print(f"Found {count} songs")
    if (not path.exists(filepath)):
        if verbose:
            print(
                f"File path does not exist, creating directory {filepath}...")
        makedirs(filepath)
    if verbose:
        print(f"Writing to file...")
    write_to_file(path.join(filepath, "output.txt"), res)


def output_custom(artist, results, count, vars):
    res = {'artist': artist, 'number': count, 'songs': []}
    for result in results:
        obj = {'Song': result['name']}
        for var in vars:
            obj[var] = result[var]
        res['songs'].append(obj)
    return res


def output_songs(artist, results, count):
    res = {'artist': artist, 'number': count, 'songs': []}
    for result in results:
        res['songs'].append(result['name'])
    return res


def output_songs_raw(artist, results, count):
    res = {'artist': artist, 'number': count, 'songs': []}
    for result in results:
        res['songs'].append(result)
    return res


def write_to_file(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
