from mvv_parser import MyRequest
from mvv_parser import MVVParser


def main():
    myreq = MyRequest('Ampfingstraße')
    print(myreq.url)
    parsed = MVVParser(myreq.content)
    lines = parsed.get_routes()
    for line in lines:
        print(line.__dict__)


if __name__ == '__main__':
    main()
