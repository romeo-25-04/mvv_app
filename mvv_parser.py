import re
import requests
from bs4 import BeautifulSoup, Tag


class MVVLine:
    def __init__(self):
        self.line = ''
        self.direction = ''
        self.duration = ''

    def __str__(self):
        return "{} {} {}".format(self.line, self.direction, self.duration)


class MyRequest:
    TRAFO = {
        'Ä': '%C4', 'Ö': '%D6', 'Ü': '%DC',
        'ä': '%E4', 'ö': '%F6', 'ü': '%FC',
        'ß': '%DF', ' ': '+'
    }
    def __init__(self, station):
        self.station = station
        payload_station = [self.TRAFO.get(c) if c in self.TRAFO.keys() else c
                           for c in station]
        payload_station = str.encode(''.join(payload_station))
        self.payload = {'ubahn': '', 'sbahn': '',
                        'bus': '', 'tram': ''}
        r = requests.get(b'https://www.mvg-live.de/ims/dfiStaticAnzeige.svc?haltestelle=' + payload_station,
                         params=self.payload)
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


class Stations:
    URL_TEMPLATE = "https://www.mvg-live.de/ims/dfiStaticAuswahl.svc?haltestelle={}"
    def __init__(self):
        self.stations = []

    def get_stations(self):
        for i in range(ord('a'), ord('z')+1):
            req = requests.get(self.URL_TEMPLATE.format(chr(i)))
            soup = BeautifulSoup(req.content, "html.parser")
            links = soup.find_all(href=re.compile("/ims/dfiStaticAnzeige"))
            stations = [elem.contents[0].strip() for elem in links]
            self.stations.extend(stations)



def tag_is_line(tag):
    return isinstance(tag, Tag) and tag.name == "tr" and tag.has_attr('class')
