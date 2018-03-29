import requests
from bs4 import BeautifulSoup, NavigableString, Tag


class MVVLine:
    def __init__(self):
        self.line = ''
        self.direction = ''
        self.duration = ''

    def __str__(self):
        return "{} {} {}".format(self.line, self.direction, self.duration)

class MyRequest:
    def __init__(self, station):
        self.payload = {'haltestelle': station,
                        'ubahn': '', 'sbahn': '',
                        'bus': '',
                        'tram': ''}
        r = requests.get('https://www.mvg-live.de/ims/dfiStaticAnzeige.svc', params=self.payload)
        self.status = r.status_code
        self.url = r.url
        self.contenttype = r.headers['content-type']
        self.encoding = r.encoding
        self.content = r.content
        self.text = r.text


class MVVParser:
    def __init__(self, text_html):
        self.content = text_html
        self.soup = BeautifulSoup(text_html, "html.parser")
        self.station = None
        self.current_time = None


    def get_routes(self):
        all_tr = self.soup.find_all(tag_is_line)
        routes = []
        for elem in all_tr:
            line = MVVLine()
            for child in elem.children:
                if isinstance(child, Tag):
                    child_class = child.get('class')
                    if child_class == ['lineColumn']:
                        line.line = child.contents[0].strip()
                    if child_class == ['stationColumn']:
                        line.direction = child.contents[0].strip()
                    if child_class == ['inMinColumn']:
                        line.duration = child.contents[0].strip()
            routes.append(line)
        return routes


def tag_is_line(tag):
    return isinstance(tag, Tag) and tag.name == "tr" and tag.has_attr('class')
