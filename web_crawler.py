import requests
from urllib.parse import urlparse, urljoin, urlunparse
from bs4 import BeautifulSoup
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor
from decorators import retry_on_network_error

CORRUPT_LINKS = set()
LINKS_DEPTH = {}


class Crawler(object):
    def __init__(self, url="https://www.guardicore.com"):
        self.url = url
        # self.link_depth = {}
        # self.corrupt_links = set()

    def start(self):
        links = self.get_links()

        LINKS_DEPTH.update({}.fromkeys(links, 1))

        links = [lnk for lnk in links if urlparse(lnk).netloc == urlparse(self.url).netloc]
        # for link in links:
        #     Thread(target=self.crawl, args=(link,)).run()
        with ThreadPoolExecutor(max_workers=2*8) as executor:
            executor.map(self.crawl, links)

    @retry_on_network_error(5)
    def get_html(self, url):
        return requests.get(url)

    def get_links(self, url=""):
        base = url or self.url
        full_links = set()
        resp = self.get_html(base)

        # Failed requests
        if resp.status_code not in range(200, 300):
            print(f"URL `{base}` returned `{resp.status_code} | {resp.reason}` !")
            CORRUPT_LINKS.add(base)
            return full_links

        for anchor in BeautifulSoup(resp.text, "html.parser").find_all("a"):
            # Check if this is a relative link
            link = anchor.get("href")

            if not link:
                continue
            # if "mailto" in link:
            #     continue

            scheme, netloc, *args = urlparse(link)

            scheme = scheme or "http"

            # filter out not HTTP links
            if not scheme.startswith("http"):
                continue
            # Join relative path with base
            if not netloc:
                link = urljoin(base, link)
            else:
                link = urlunparse((scheme, netloc, *args))

            full_links.add(link)

        return full_links

    def crawl(self, url="", depth=2):
        url = url or self.url
        for link in self.get_links(url):
            if not LINKS_DEPTH.get(link):
                # print(link)
                LINKS_DEPTH[link] = depth
                # Update link depth - for next iteration
                depth += 1
                # Ignore non root URLs
                if urlparse(link).netloc == urlparse(url).netloc:
                    self.crawl(link, depth=depth)


if __name__ == "__main__":
    crawler = Crawler("https://www.guardicore.com")

    crawler.start()
    pprint(crawler.link_depth)
    pprint(crawler.CORRUPT_LINKS)
