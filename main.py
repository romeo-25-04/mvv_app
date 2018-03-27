import requests


def main():
    payload = {'haltestelle': 'Hauptbahnhof',
               'ubahn': '',
               'sbahn': '',
               'bus': '',
               'tram': ''}
    r = requests.get('https://www.mvg-live.de/ims/dfiStaticAnzeige.svc', params=payload)
    print("Status code:\t", r.status_code)
    print("request at:\t", r.url)
    print("content-type:\t", r.headers['content-type'])
    print("encoding:\t", r.encoding)
    print('text:\t', r.text)


if __name__ == '__main__':
    main()
