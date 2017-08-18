#!/usr/bin/env python3
"""gets podcast from webpage."""
from pprint import pprint
import urllib
import urllib.request
import sys
import hashlib
import re
import requests


class Podcast(object):
    """class gets the podcasts."""

    def __init__(self, page_url):
        """method calls the self and page_url variables."""
        self.page_url = page_url
        self.urls_on_page = get_urls(self.page_url)

    def lucy_mp3(self):
        """method finds urls with mp3 in them and creates a file."""
        mp3_urls = []
        download_dir = '/home/kevin/Desktop/podcast'

        for url in self.urls_on_page:
            print('0000000000', url)
            mp3_urls.extend(get_urls(url, mp3_only=True))
            for next_mp3_url in mp3_urls:
                if next_mp3_url.endswith('.mp3'):
                    print('666666', next_mp3_url)
                    # split url for name of podcast as part of file name
                    file_name = next_mp3_url.split('/')[-2]
                    file_name = '{}/{}.mp3'.format(download_dir, file_name)
                    with urllib.request.urlopen(next_mp3_url) as response:
                        data = response.read()
                    with open(file_name, 'wb') as out_file:
                        print('888888888')
                        out_file.write(data)
                    # test it out with one page first
                    # sys.exit(1)

    def next_page(self):
        """method moves on to the next page of the website."""
        needed_urls = []
        # puts all the next page urls into the file
        next_page_list = []

        for url in self.urls_on_page:
            needed_urls.extend(get_urls(url, mp3_only=False))
            for next_page in needed_urls:
                if 'page=' in next_page:
                    print('1111111111')
                    next_page_list.append(next_page)
                    print('222222222', next_page_list)
                    break


def get_urls(url, mp3_only=False):
    """function" will download raw date from page to console."""
    # use a user agent to go through the website
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1'
        ') AppleWebKit/537.36 (KHTML, like Gecko'
        ') Chrome/39.0.2171.95 Safari/537.36'}

    # sift through the page using different user agent and decoded data
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as data:
        html = data.read().decode('utf-8')

    lines = html.split('\n')
    # the first part of the url
    head = 'https://www.ft.com'
    # list to append all the needed urls to
    needed_urls = []
    mp3_urls = []

    # sift through html data
    for line in lines:
        if 'href=' in line:
            items = line.split()
            for raw_item in items:
                item = raw_item.replace('"', '')
                if 'href=' in item:
                    # find the href with content and next page/turn into url
                    if mp3_only is False:
                        if '/content/' in item:
                            content = item.replace('href=', '')
                            content_url = '{}{}'.format(head, content)
                            needed_urls.append(content_url)
                            # print('555555555', content_url)
                        elif '?page&#x3D;' in item:
                            next_pg = item.replace('href=', '')
                            next_pg_url = '{}/{}'.format(head, next_pg)
                            needed_urls.append(next_pg_url)
                            # print('33333333', next_pg_url)
                    else:
                        # the second version of mp3_only, uses mp3s
                        if '.mp3' in item:
                            mp3 = item.replace('href=', '')
                            full_mp3 = mp3.replace('>download', '')
                            mp3_urls.append(full_mp3)
                            return mp3_urls

    # take out the duplicates
    needed_urls = set(needed_urls)
    # pprint(needed_urls)
    return needed_urls


def main():
    """impliment the code."""
    # first page to look at
    url = 'https://www.ft.com/listen-to-lucy'

    podcast = Podcast(url)
    # podcast.lucy_mp3()
    podcast.next_page()


if __name__ == '__main__':
    main()
