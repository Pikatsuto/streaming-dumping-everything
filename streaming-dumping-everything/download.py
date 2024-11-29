from time import sleep
from random import randrange
from multiprocess import Pool
import yt_dlp
import os
import json


class Download:
    def __init__(self) -> None:
        self.data = {}

        if os.path.exists("./data.json"):
            with open("./data.json", "r") as file:
                self.data = json.loads(file.read())

    def download_video(self, url, path):
        ydl_opts = {
            'format':
                'webm[height=1080],'
                'mp4[height=1080],'
                'webm[height=720],'
                'mp4[height=720]',
            'outtmpl': path + '.%(ext)s'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def scan_json(self):
        def download_episode(episode):
            for lecteur in episode["episode"]:
                try:
                    os.system(f"mkdir -p './data/{episode['path']}'")
                    self.download_video(
                        lecteur,
                        f"./data/{episode['fullPath']}"
                    )
                    break
                except Exception:
                    sleep(randrange(2, 4))

        with Pool(processes=6) as pool:
            for episodeId in self.data:
                episode = self.data[episodeId]
                sleep(randrange(2, 4))
                pool.apply_async(download_episode, (episode,))

            pool.close()
            pool.join()

    def start(self) -> None:
        self.scan_json()
