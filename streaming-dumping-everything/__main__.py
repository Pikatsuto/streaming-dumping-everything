from scan import Scan
from download import Download
from threading import Thread
from time import sleep


class Main:
    def __init__(self) -> None:
        pass

    def start_scan(self) -> None:
        print("Start Scrapping")
        scan = Scan()
        scan.start()
        print("End Scrapping")

    def start_download(self, scan) -> None:
        print("Start Download")

        while scan.is_alive():
            download = Download()
            download.start()

        print("End Download")

    def start(self,) -> None:
        while True:
            print("Start Programe")

            scan = Thread(target=self.start_scan)
            scan.start()

            download = Thread(target=self.start_download, args=(scan,))
            download.start()
            download.join()

            print("End Programe")

            print('Sleep 2h before next loop')
            sleep(7200)

if __name__ == "__main__":
    main = Main()
    main.start()
