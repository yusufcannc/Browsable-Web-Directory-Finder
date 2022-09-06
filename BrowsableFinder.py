import argparse
import re
from time import sleep
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
                    req = requests.get(url, timeout=5, verify=False)
                    soup = BeautifulSoup(req.content, "html.parser")
                    redirectFind = soup.find("meta",attrs={"http-equiv":"refresh"})
                    redirect_re = re.compile('<meta[^>]*?url=(.*?)["\']', re.IGNORECASE)
                    match = redirect_re.search(str(redirectFind))
                    try:
                        if match:
                            new_url =  url + "/" + match.groups()[0].strip()
                        
                            req_refresh = requests.get(new_url, timeout=5, verify=False)
                            soup_refresh = BeautifulSoup(req_refresh.content, "html.parser")
                            if "Index of" in str(soup_refresh.title)  or  "[PARENTDIR]" in str(soup_refresh):
                                print("Found Index of " + new_url)
                            else:
                                self.getCSSLinks(soup_refresh)
                                self.getJSlinks(soup_refresh)
                                self.getImg(soup_refresh)
                                self.pathRequests(url)
                                self.paths.clear()
                    
                        else:
                            if "Index of" in str(soup.title):
                                print("Found Index of " + url)
                            else:
                                self.getCSSLinks(soup)
                                self.getJSlinks(soup)
                                self.getImg(soup)
                                self.pathRequests(url)
                                self.paths.clear()
                    except AttributeError:
                        pass
                except requests.exceptions.ConnectionError as err:
                    pass
                except requests.exceptions.ReadTimeout as err:
                    pass
                except requests.exceptions.TooManyRedirects as err:
                    pass
                except requests.exceptions.InvalidURL as err:
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
                elif link.get("src").startswith("data:"):
                    pass
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
            req = requests.get(url + i, verify=False)
            
            html = BeautifulSoup(req.text, "html.parser")
            if  "Index of" in str(html.title) or  "[PARENTDIR]" in str(html):
                print("Found Index of " + url + i)
            else:
                pass

if __name__ == "__main__":
    app = AllGetLink()
