from time import sleep
from random import randrange
from multiprocess import Pool
import yt_dlp
import os
import json


class Download:
    def __init__(self, nb_thread) -> None:
        self.nb_thread = nb_thread
        self.data = {}

        for i in range(0, 10):
            try:
                if os.path.exists("./data/scan.json"):
                    with open("./data/scan.json", "r") as file:
                        self.data = json.loads(file.read())
                break
            except Exception:
                continue

    def download_video(self, url, path, folder, lang):
        videos_path_with_extentions = [
            path + ".mp4",
            path + ".webm"
        ]

        for video_path in videos_path_with_extentions:
            print(video_path)
            if os.path.exists(video_path):
                return

        name = path.split("/")[-1].split(" ")
        name.pop(-1)
        name = " ".join(name)

        for i in os.listdir(folder):

            old_lang: str = i.split(".")[0].split(" ")[-1]
            old_name = i.split(" ")
            old_name.pop(-1)
            old_name = " ".join(old_name)

            if old_lang != "VF" and lang == "VF" and old_name == name:
                print(f"delete VO from VF : {path}")
                os.remove(folder + i)

        ydl_opts = {
            'format':
                'webm[height=1080],'
                'mp4[height=1080],'
                'webm[height=720],'
                'mp4[height=720],'
                'best',
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
                        f"./data/{episode['fullPath']}",
                        f"./data/{episode['path']}",
                        episode['lang'],
                    )
                    break
                except Exception:
                    sleep(randrange(2, 4))

        with Pool(processes=self.nb_thread) as pool:
            for episodeId in self.data:
                episode = self.data[episodeId]
                sleep(randrange(2, 4))
                pool.apply_async(download_episode, (episode,))

            pool.close()
            pool.join()

    def start(self) -> None:
        self.scan_json()
