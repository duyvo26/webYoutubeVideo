from youtubesearchpython import *
import urllib.parse
from lxml import etree
import bs4
import sys  # import sys package
import re
import requests

sys.path.pop(0)


def get_html_from_url(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()  # Raise an exception for unsuccessful responses
    return response.text


def extract_youtube_url(link_tag):
    if link_tag and "youtube.com/watch":
        url_match = re.search(r"url=([^&]+)", link_tag["href"])
        if url_match:
            url = url_match.group(1)
            decoded_url = urllib.parse.unquote(url)
            return decoded_url
    return None


def getImg(url):
    videoInfo = Video.getInfo(url, mode=ResultMode.json)
    # print("videoInfo", videoInfo["thumbnails"][1]["url"])
    return videoInfo["thumbnails"][1]["url"]


def extract_text_from_xpath(response_text):
    soup = bs4.BeautifulSoup(response_text, "html.parser")
    youtube_links = []
    for index, tag in enumerate(soup.find_all("a", href=True)):
        if "https://www.youtube.com/watch" in tag["href"]:
            img = getImg(extract_youtube_url(tag))

            if len(tag.text) > 2:
                youtube_links.append(
                    [extract_youtube_url(tag), tag.text.split("- YouTubewww")[0], img]
                )

    return youtube_links


def extract_data_image_src(html_content):
    for i in str(html_content).split(" "):
        if "data-url=" in i:
            return i.replace('"', "").replace("src=", "")