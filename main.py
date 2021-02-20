import requests
import sys
import re
from urllib.parse import urlparse
import collections
import json

class WebCrawler():
    def __init__(self, start_url, max_depth):
        self.start_url = start_url
        self.max_depth = int(max_depth)
        self.visited = set()

    def get_html(self, url):
        # request the URL and return its contents
        try:
            html = requests.get(url)
        # an exception handler here avoids that the program breaks in case it cannot visit a URL
        except Exception as e:
            print(e)
            return ""
        return html.content.decode('latin-1')

    def get_links(self, url):
        # URL is requested calling `get_html()` method
        html = self.get_html(url)
        # URL string is parsed for scheme and netloc extraction
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        # links are searched in the crawled page using a regular expression that returns 'href' values of <a> nodes
        links = re.findall('<a\s+(?:[^>]*?\s+)?href="([^"]*)"', html)
        # every link which has no scheme and netloc inherits them from its parent url
        for i, link in enumerate(links):
            if not urlparse(link).netloc:
                link_with_base = base + link
                links[i] = link_with_base
        # the method returns a (unique) set of links filtered by start_url
        return {x for x in links if base in x and 'mailto' not in x}

    def crawl(self, start_url, max_depth):
        data = dict()
        # 'start_url' gets assigned depth 0
        depth = {start_url: 0}
        # it is enqueued and added to the visited urls
        queue = collections.deque([start_url])
        self.visited.add(start_url)

        # the crawling will carry on as long as the queue is not empty - limited to 'max_depth'
        while queue:
            # the URL to the left of the queue is popped and checked for depth
            v = queue.popleft()
            if depth[v] == max_depth:
                break
            print(f'<{v}>')

            # 'get_links()' method is called to extract the links
            urls = self.get_links(v)
            # for each URL in the result, check if has been visited already, otherwise add it to visited urls and enqueue it
            for url in urls:
                if url not in self.visited:
                    self.visited.add(url)
                    queue.append(url)
                    # assemble the dictionary 'data'
                    if v in data:
                        data[v].append(url)
                    else:
                        data[v] = [url]
                    # assign URL depth
                    depth[url] = depth[v] + 1
                    print(f'\t<{url}>')

        # results are saved to 'data.json'
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print('\nCrawling finished successfully!\n')

    def start(self):
        self.crawl(self.start_url, self.max_depth)


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print('Missing arguments. Abort.')
        sys.exit()
    if int(sys.argv[2]) == 0:
        print(f'<{sys.argv[1]}>')
        print(f'Please input a depth 1 or above in order to follow URLs.')
        sys.exit()

    crawler = WebCrawler(start_url=sys.argv[1], max_depth=sys.argv[2])
    crawler.start()
