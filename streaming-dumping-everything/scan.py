from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from multiprocess import Process, Pipe
import subprocess
import os
import json
import re


class Scan:
    def __init__(self) -> None:
        service = webdriver.ChromeService(
            executable_path=os.environ["CHROMEDRIVER"])

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')

        self.driver = webdriver.Chrome(service=service, options=options)
        self.force_rescan = False

    def system_run(self, command: str) -> str:
        return subprocess.check_output(command, shell=True, text=True)

    def load_pages(self, uri: str, handling=None) -> BeautifulSoup:
        def process(connection) -> BeautifulSoup:
            self.driver.get(uri)
            content = BeautifulSoup(self.driver.page_source, 'html.parser')
            if handling:
                content = handling(content)

            connection.send(content)

        for i in range(3):
            conn1, conn2 = Pipe()
            p = Process(target=process, args=(conn2,))
            p.start()
            p.join(timeout=10)
            value = conn1.recv()
            if p.is_alive():
                p.terminate()
                continue

            return value

        print("Error: Time out scrapping")
        exit(1)

    def full_name(self, string: str) -> str:
        return (re.sub(
            "[A-Za-z]+", lambda ele: " " + ele[0] + " ",
            string
        ).title())[1:].replace(" - ", "-")

    def text_formated(self, sup: BeautifulSoup, selector: str) -> str:
        return f"{sup.select(selector)[0].get_text()}".replace("/", "-")

    def extract_from_url(self, string: str, index: int) -> str:
        return string.split("/")[index]

    def extract_number_str(self, string: str) -> str:
        numbers = re.findall(r'\d+', string)
        value = "-".join(numbers)
        if len(numbers) == 1:
            value = f"{int(numbers[0]):02d}"

        return value

    def selectHtmlParser(
        self,
        content: BeautifulSoup,
        select_id: str,
        targed_selector: str = None,
        target_content: str = None,
        re_run_in_args: list = None,
    ) -> list:
        select = Select(self.driver.find_element(by=By.ID, value=select_id))
        options = content.select(f"#{select_id} option")

        targetArray = []
        for index, name in enumerate(options):
            select.select_by_index(index)

            selector = "*"
            if targed_selector:
                selector = targed_selector

            sup = BeautifulSoup(
                self.driver.page_source,
                'html.parser'
            )
            value = sup.select(selector)[0]
            if target_content:
                value = value[target_content]

            if re_run_in_args:
                value = self.selectHtmlParser(
                    *re_run_in_args
                )

            targetArray.append(value)

        return targetArray

    def get_episodes(
        self,
        data,
        host,
        serie,
        saisonNumber,
        serieFullName,
        saisonFullName,
        lang,
        saisonName,
        saisonUri,
    ):

        def handling(content: BeautifulSoup):
            re_run_in_args = [
                content,
                "selectLecteurs",
                "iframe#playerDF",
                "src",
            ]

            return self.selectHtmlParser(
                content=content,
                select_id="selectEpisodes",
                re_run_in_args=re_run_in_args,
            )

        episodes_uris = self.load_pages(saisonUri, handling)

        for index, lecteurs in enumerate(episodes_uris):
            episodeNumber = f"{index+1:02d}"
            identifier = f"{host}/{serie}/S{saisonNumber}E{episodeNumber}"
            title = f"{serieFullName} S{saisonNumber} E{episodeNumber} {lang}"
            path = f"{serieFullName}/{saisonFullName}"
            fullPath = f"{path}/{title}"

            if (
                identifier in data
                and data[identifier]["lang"] != "vf"
                and lang == "vf"
            ) or identifier not in data:
                value = {identifier: {
                    "serie": serie,
                    "serieFullName": serieFullName,
                    "saison": saisonName,
                    "saisonFullName": saisonFullName,
                    "saisonUri": saisonUri,
                    "saisonNumber": saisonNumber,
                    "lang": lang,
                    "title": title,
                    "path": path,
                    "fullPath": fullPath,
                    "episode": lecteurs,
                }}
                data.update(value)

                print(f"write {identifier} in scan.json")
                with open("./data/scan.json", "w+") as file:
                    file.write(json.dumps(data, indent=2))

        return data

    def get_saisons(self) -> object:
        data = {}
        if not os.path.exists("./data"):
            os.mkdir("./data")
        if os.path.exists("./data/scan.json"):
            with open("./data/scan.json", "r") as file:
                data = json.loads(file.read())

        saisons_links = self.load_pages("https://anime-sama.fr/")
        saisons_links = saisons_links.select("div#containerAjoutsAnimes a")

        for saison in saisons_links:
            saisonUri = saison["href"]
            saisonName = self.extract_from_url(saisonUri, 5)

            if saisonName == "film":
                continue

            saisonFullName = (self.full_name(saisonName))
            saisonNumber = self.extract_number_str(saisonFullName)
            host = self.extract_from_url(saisonUri, 2)
            lang = self.extract_from_url(saisonUri, -2).upper()
            serie = self.extract_from_url(saisonUri, 4)
            serieFullName = self.text_formated(saison, "h1")

            self.get_episodes(
                data,
                host,
                serie,
                saisonNumber,
                serieFullName,
                saisonFullName,
                lang,
                saisonName,
                saisonUri,
            )

        return data

    def start(self) -> None:
        self.get_saisons()
