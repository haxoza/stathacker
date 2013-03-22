import requests
from pyquery import PyQuery as pq


class Hackernews(object):
    start_url = 'https://news.ycombinator.com/'
    pages_to_crawl = 3

    def __init__(self):
        self.items = []

    def run(self):
        url = self.start_url
        for _ in xrange(self.pages_to_crawl):
            response = requests.get(url)
            parser = HackernewsParser(response.content)
            parser.parse()
            self.items.extend(parser.get_items())
            url = self.start_url + parser.get_next_url()

    def get_items(self):
        return self.items


class HackernewsParser(object):

    def __init__(self, content):
        self.content = content
        self.items = []
        self.next_url = None

    def parse(self):
        d = pq(self.content)
        titles = d('td.title')
        for title in titles:
            d = pq(title)
            anchor = d('a')
            domain = d('.comhead').text()
            if anchor:
                self.items.append({
                    'title': anchor.text(),
                    'url': anchor.attr('href'),
                    'domain': domain[1:-1] if domain else None
                })
        last_item = self.items.pop()
        self.next_url = last_item['url']
        if self.next_url[0] == '/':
            self.next_url = self.next_url[1:]

    def get_items(self):
        return self.items

    def get_next_url(self):
        return self.next_url


if __name__ == '__main__':
    news = Hackernews()
    news.run()
    print(news.get_items())
