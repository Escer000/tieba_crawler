from bs4 import BeautifulSoup
import re
import urllib.parse

class HtmlParser (object):
    def _get_new_urls(self, page_url, soup):
        # /view/123.htm
        new_urls = set ( )
        links = soup.find_all ('a', href=re.compile (r"/v\d+\.htm"))
        for link in links:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin (page_url, new_url)
            new_urls.add (new_full_url)
            # print(new_urls)
            return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {}

        # url
        res_data['url'] = page_url

        # <>
        title_node = soup.find ('div', class_="lemma_name").find ("h1")
        res_data['title'] = title_node.get_text ( )

        # <>
        summary_node = soup.find ('div', class_="abstract")
        res_data['summary'] = summary_node.get_text ( )

        return res_data

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup (html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls (page_url, soup)
        new_data = self._get_new_data (page_url, soup)
        return new_urls, new_data