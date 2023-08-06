from bs4 import BeautifulSoup
import requests, html, re

class SoundCloud:
    def __init__(self, url):
        self._url_ = url
        self.__regex__url_sound_cloud = re.match(r"https?://(soundcloud.com|snd.sc)\/(.*)", url)
        self._headers_ ={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
         
    @property
    def title(self):
        if not self.__regex__url_sound_cloud:
            return "Invaild url format (Music-debugger) (i.e https://soundcloud.com/jonbellion/all-time-low-new-mix)"
        req = requests.get(self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="og:title").get('content'))

    @property
    def type(self):
        if not self.__regex__url_sound_cloud:
            return "Invaild url format (Music-debugger) (i.e https://soundcloud.com/jonbellion/all-time-low-new-mix)"
        req = requests.get(self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="og:type").get('content'))

    @property
    def description(self):
        if not self.__regex__url_sound_cloud:
            return "Invaild url format (Music-debugger) (i.e https://soundcloud.com/jonbellion/all-time-low-new-mix)"
        req = requests.get(
            self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="og:description").get('content'))

    @property
    def like_count(self):
        if not self.__regex__url_sound_cloud:
            return "Invaild url format (Music-debugger) (i.e https://soundcloud.com/jonbellion/all-time-low-new-mix)"
        req = requests.get(
            self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return format(int(html.unescape(soup.find("meta", property="soundcloud:like_count").get('content'))), ',d')

    @property
    def play_count(self):
        if not self.__regex__url_sound_cloud:
            return "Invaild url format (Music-debugger) (i.e https://soundcloud.com/jonbellion/all-time-low-new-mix)"
        req = requests.get(
            self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return format(int(html.unescape(soup.find("meta", property="soundcloud:play_count").get('content'))), ',d')

    @property
    def download_count(self):
        if not self.__regex__url_sound_cloud:
            return "Invaild url format (Music-debugger) (i.e https://soundcloud.com/jonbellion/all-time-low-new-mix)"
        req = requests.get(
            self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return format(int(html.unescape(soup.find("meta", property="soundcloud:download_count").get('content'))), ',d')

    @property
    def comments_count(self):
        if not self.__regex__url_sound_cloud:
            return "Invaild url format (Music-debugger) (i.e https://soundcloud.com/jonbellion/all-time-low-new-mix)"
        req = requests.get(
            self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return format(int(html.unescape(soup.find("meta", property="soundcloud:comments_count").get('content'))), ',d')

    @property
    def artist(self):
        if not self.__regex__url_sound_cloud:
            return "Invaild url format (Music-debugger) (i.e https://soundcloud.com/jonbellion/all-time-low-new-mix)"
        req = requests.get(
            self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="soundcloud:user").get('content'))

    @property
    def image(self):
        if not self.__regex__url_sound_cloud:
            return "Invaild url format (Music-debugger) (i.e https://soundcloud.com/jonbellion/all-time-low-new-mix)"
        req = requests.get(self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="og:image").get('content'))
    
    def __str__(self):
        return f"Title: {self.title}\nType: {self.type}\nDescription: {self.description}\nLike Count: {self.like_count}\nPlay Count: {self.play_count}\nDownload Count: {self.download_count}\nComments Count: {self.comments_count}\nArtist: {self.artist}\nImage: {self.image}"