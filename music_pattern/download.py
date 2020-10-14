# -*- coding:utf-8 -*-
import os
import requests
from tqdm import tqdm
from urllib.request import urlopen


def download(url, path):
    if os.path.exists(path):
        os.remove(path)

    try:
        file_size = int(urlopen(url).info().get('Content-Length', -1))
        first_byte = 0

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Inter Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        pbar = tqdm(total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=path)
        req = requests.get(url, headers=headers, timeout=60, stream=True)

        with open(path, 'ab') as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
        pbar.close()
        print("download complete!, file size = {}".format(file_size))

    except:
        if os.path.exists(path):
            os.remove(path)
        raise Exception ("Invalid url: {}".format(url))

