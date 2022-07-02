import argparse


import requests
import tldextract
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AllGetLink:
    def __init__(self):
        self.paths = []
        self.urls = []
        parser = argparse.ArgumentParser()
        parser.add_argument("--file", "-f", help="File name of urls\n")
        self.filename = parser.parse_args()
        self.getURLS()
        self.getReq()

    def getURLS(self):
        with open(self.filename.file, "r+") as file:
            for i in file:
                self.urls.append(i.split("\n")[0])

    def getReq(self):
        for url in self.urls:
            try:
                self.extract = tldextract.extract(url)
                self.domain = (
                    self.extract.domain
                )  # The reason for separating domains is to search only for this domain in links and scripts.
                req = requests.get(url, timeout=5)
                soup = BeautifulSoup(req.content, "html.parser")
                self.getCSSLinks(soup)
                self.getJSlinks(soup)
                self.getImg(soup)
                self.pathRequests(url)

                self.paths.clear()
            except requests.exceptions.ConnectionError:
                pass
            except requests.exceptions.ReadTimeout:
                pass

    def getCSSLinks(self, url):
        for link in url.find_all("link"):
            if link.get("href") != None:
                if "http" in link.get("href"):
                    firstPath = link.get("href").split("/")
                    if firstPath in self.paths:
                        pass
                    else:
                        res = "/"
                        a = 0
                        for i in range(3, len(firstPath) - 1):

                            for j in firstPath[3 + a : i]:
                                res = res + j + "/"
                                a += 1
                            if res in self.paths:
                                pass
                            else:
                                self.paths.append(res)

                else:
                    firstPath = link.get("href").split("/")
                    if firstPath in self.paths:
                        pass
                    else:
                        res = "/"
                        a = 0
                        for i in range(0, len(firstPath) - 1):

                            for j in firstPath[0 + a : i]:
                                res = res + j + "/"
                                a += 1
                            if res in self.paths:
                                pass
                            else:
                                self.paths.append(res)

    def getJSlinks(self, url):
        for link in url.find_all("script"):
            if link.get("src") != None:
                if "http" in link.get("src"):

                    firstPath = link.get("src").split("/")
                    if firstPath in self.paths:
                        pass
                    else:
                        res = "/"
                        a = 0
                        for i in range(3, len(firstPath) - 1):

                            for j in firstPath[3 + a : i]:
                                res = res + j + "/"
                                a += 1
                            if res in self.paths:
                                pass
                            else:
                                self.paths.append(res)

                else:
                    firstPath = link.get("src").split("/")
                    if firstPath in self.paths:
                        pass
                    else:
                        res = "/"
                        a = 0
                        for i in range(0, len(firstPath) - 1):

                            for j in firstPath[0 + a : i]:
                                res = res + j + "/"
                                a += 1
                            if res in self.paths:
                                pass
                            else:
                                self.paths.append(res)

    def getImg(self, url):
        for link in url.find_all("img"):
            if link.get("src") != None:

                if "http" in link.get("src"):

                    firstPath = link.get("src").split("/")
                    if firstPath in self.paths:
                        pass
                    else:
                        res = "/"
                        a = 0
                        for i in range(3, len(firstPath) - 1):
                            for j in firstPath[3 + a : i]:
                                res = res + j + "/"
                                a += 1
                            if res in self.paths:
                                pass
                            else:
                                self.paths.append(res)
                else:
                    firstPath = link.get("src").split("/")
                    if firstPath in self.paths:
                        pass
                    else:
                        res = "/"
                        a = 0
                        for i in range(0, len(firstPath) - 1):

                            for j in firstPath[0 + a : i]:
                                res = res + j + "/"
                                a += 1
                            if res in self.paths:
                                pass
                            else:
                                self.paths.append(res)

    def pathRequests(self, url):
        for i in self.paths:
            req = requests.get(url + i)
            html = BeautifulSoup(req.text, "html.parser")
            if "Index of" in str(html.title):
                print("Found Index of" + url + i)
            else:
                pass


if __name__ == "__main__":
    app = AllGetLink()
