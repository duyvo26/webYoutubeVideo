from youtubesearchpython import Video as VideoYoutuve, ResultMode
import urllib.parse
from lxml import etree
import bs4
import sys  # import sys package
import re
import requests
import certifi

sys.path.pop(0)


class Video:
    def __init__(self) -> None:
        pass

    def get_html_from_url(self, url):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, verify=False)
        return response.text

    def extract_youtube_url(self, link_tag):
        if link_tag:
            url_match = re.search(r"url=([^&]+)", link_tag["href"])
            if url_match:
                decoded_url = urllib.parse.unquote(url_match.group(1))
                return decoded_url
        return None

    def getInfo(self, url):
        videoInfo = VideoYoutuve.getInfo(url, mode=ResultMode.json)  # type: ignore
        # print("videoInfo", videoInfo)
        return videoInfo["thumbnails"][1]["url"], videoInfo["id"]

    def extract_text_from_xpath(self, response_text):
        soup = bs4.BeautifulSoup(response_text, "html.parser")
        youtube_links = []
        for index, tag in enumerate(soup.find_all("a", href=True)):
            if "https://www.youtube.com/watch" in tag["href"]:
                if len(tag.text) > 2:
                    data_ = self.getInfo(self.extract_youtube_url(tag))
                    data = {
                        "href": data_[1],
                        "title": tag.text.split("- YouTubewww")[0],
                        "img": data_[0],
                    }
                    youtube_links.append(data)
        return youtube_links

    def extract_data_image_src(self, html_content):
        for i in str(html_content).split(" "):
            if "data-url=" in i:
                return i.replace('"', "").replace("src=", "")
