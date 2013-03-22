import re
import requests
from pyquery import PyQuery as pq


class Hackernews(object):
    start_url = 'https://news.ycombinator.com/'

    def __init__(self):
        self.items = []
        self.filtered_items = None

    def run(self, keyword, pages=1):
        self.crawl(pages)
        self.analyze(keyword)

    def crawl(self, pages):
        url = self.start_url
        for _ in xrange(pages):
            response = requests.get(url)
            parser = HackernewsParser(response.content)
            parser.parse()
            self.items.extend(parser.get_items())
            url = self.start_url + parser.get_next_url()

    def analyze(self, keyword):
        analyzer = HackernewsAnalyzer([keyword], self.items)
        self.filtered_items = analyzer.analyze()

    def get_items(self):
        return self.items

    def get_results(self):
        return self.filtered_items


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


class HackernewsAnalyzer(object):

    def __init__(self, words, items):
        self.words = words
        self.items = items
        self.results = []

    def analyze(self):
        results = set()
        patterns = [re.compile(r'.*{word}.*'.format(word=re.escape(w)), re.IGNORECASE) for w in self.words]
        for item in self.items:
            for key, value in item.iteritems():
                for p in patterns:
                    if value and p.match(value):
                        results.add(tuple(item.items()))
        self.results = [dict(item) for item in results]
        return self.results


if __name__ == '__main__':
    news = Hackernews()
    news.run('ruby', 3)
    print(news.get_results())
