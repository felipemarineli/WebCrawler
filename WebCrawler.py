import requests
import sys
import re
from urllib.parse import urlparse
import collections
import json

class WebCrawler():
    # Constructor
    def __init__(self, start_url, max_depth):
        self.start_url = start_url
        self.max_depth = int(max_depth)
        self.visited = set()

    def get_html(self, url):
        try:
            html = requests.get(url)
        # An exception handler here avoids that the program breaks in case it cannot visit a URL
        except Exception as e:
            print(e)
            return ""
        return html.content.decode('latin-1')

    def get_links(self, url):
        # url is requested calling `get_html()` method
        html = self.get_html(url)
        # url string of the crawled URL is parsed for scheme and netloc extraction
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        # links are searched in the crawled HTML using a regular expression that returns 'href' values of <a> nodes
        links = re.findall('<a\s+(?:[^>]*?\s+)?href="([^"]*)"', html)
        # every link found which has no netloc inherits it from its parent url
        for i, link in enumerate(links):
            if not urlparse(link).netloc:
                link_with_base = base + link
                links[i] = link_with_base
        # the method finally returns a unique set of links filtered by start_url
        return {x for x in links if base in x and 'mailto' not in x}

    def crawl(self, start_url, max_depth):
        data = dict()
        depth = {start_url: 0}
        queue = collections.deque([start_url])
        self.visited.add(start_url)

        # The crawling ends once it does not find any new urls to queue up within max_depth.
        while queue:
            v = queue.popleft()
            if depth[v] == max_depth:
                break
            print(f'<{v}>')

            urls = self.get_links(v)
            for url in urls:
                if url not in self.visited:
                    self.visited.add(url)
                    queue.append(url)
                    if v in data:
                        data[v].append(url)
                    else:
                        data[v] = [url]
                    depth[url] = depth[v] + 1
                    print(f'\t<{url}>')

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def start(self):
        self.crawl(self.start_url, self.max_depth)


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print('Missing arguments. Abort.')
        sys.exit()

    crawler = WebCrawler(start_url=sys.argv[1], max_depth=sys.argv[2])
    crawler.start()
