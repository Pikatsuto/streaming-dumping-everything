from scan import Scan
from download import Download
from threading import Thread
from argparse import ArgumentParser
from time import sleep


class Main:
    def __init__(self) -> None:
        parser = ArgumentParser()
        parser.add_argument("-s", "--scan",
                            help="Start the scan", action="store_true")
        parser.add_argument("-d", "--download",
                            help="Start the download", action="store_true")
        parser.add_argument("-t", "--threads", type=int,
                            help="Number of thread to use", default=6)
        self.args = parser.parse_args()

    def start_scan(self) -> None:
        print("Start Scrapping")
        scan = Scan()
        scan.start()
        print("End Scrapping")

    def start_download(self, scan, nb_thread) -> None:
        print("Start Download")

        if scan is None:
            download = Download(nb_thread)
            download.start()

        else:
            while scan.is_alive():
                download = Download(nb_thread)
                download.start()

        print("End Download")

    def start(self,) -> None:
        print("Start Programe")

        while True:
            if self.args.scan:
                scan = Thread(target=self.start_scan)
                scan.start()

            if self.args.download and self.args.scan:
                download = Thread(
                    target=self.start_download,
                    args=(scan, self.args.threads)
                )
                download.start()
            elif self.args.download and not self.args.scan:
                download = Thread(
                    target=self.start_download,
                    args=(None, self.args.threads)
                )
                download.start()

            if self.args.scan and not self.args.download:
                scan.join()
            elif self.args.download:
                download.join()

            print('Sleep 2h before next loop')
            sleep(7200)

        print("End Programe")


if __name__ == "__main__":
    main = Main()
    main.start()
