#!/usr/bin/env python3

"""
FAZ-paperboy delivers your FAZ or F.A.S. newspaper freshly every day.
"""

try:
    from bs4 import BeautifulSoup
    import requests
    ext_deps = True
except ImportError:
    ext_deps = False
import random
import http.cookiejar
import time
import os
import sys
import stat
import logging

def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--user-agent', '-ua', required=True, help='User agent you want paperboy to use.')
    parser.add_argument('--output-directory', '-o', required=True, help='Directory to store the PDFs of the downloaded newspaper issues.')
    parser.add_argument('--username', '-u', required=True, help='User name to login at http://faz.net for the e-paper download.')
    parser.add_argument('--password', '-p', required=True, help='Password for user given by --username.')
    parser.add_argument('--cookie-file', '-c', help='File to store the cookies in.', default='~/.FAZ-paperboy_cookies.txt')
    parser.add_argument('--debug', '-d', action='store_true', help='Increase verbosity.')

    if not ext_deps: parser.error("Missing at least one of the python modules 'requests' or 'beautifulsoup4'.")

    args = parser.parse_args()

    if args.debug: level = logging.DEBUG
    else: level = logging.INFO
    logging.basicConfig(level=level, format='%(levelname)-8s %(message)s')
    logging.getLogger("requests").setLevel(logging.WARNING)

    browser = Browser(args.user_agent, os.path.expanduser(args.cookie_file))

    random_sleep()
    index_page = browser.get('http://www.faz.net')
    # With the index_page alone we cannot easily find out if we are logged in or not...
    # A JS function replaces the login button by the user name depending on a cookie:
    # function LoginDecorator
    # in http://www.faz.net/5.9.8/js/all_scripts.min.js

    random_sleep()

    login_page = browser.get('https://www.faz.net/mein-faz-net/?redirectUrl=%2Faktuell%2F')
    random_sleep()
    logged_in = len(BeautifulSoup(login_page.text).select('span.Username')) > 0

    if logged_in:
        logging.info("Already logged in.")
    else:
        logging.info("Not logged in yet, trying to log in.")
        login_data = {
          'loginUrl': '/mein-faz-net/',
          'redirectUrl': '/aktuell/',
          'loginName': args.username,
          'password': args.password,
          'rememberMe': 'on'
        }
        login_answer = browser.post('https://www.faz.net/membership/loginNoScript', data=login_data)

        login_page = browser.get('https://www.faz.net/mein-faz-net/?redirectUrl=%2Faktuell%2F')
        logged_off = len(BeautifulSoup(login_page.text).select('span.Username')) == 0

        if logged_off:
            logging.error('Incorrect credentials?')
            sys.exit(1)

    random_sleep()
    epaper = browser.get('http://www.faz.net/e-paper/')

    newspapers = ('FAZ', 'FAS')
    produkttypen = ('FAZ', 'FAZ_RMZ', 'FAS')
    issues = dict()
    for newspaper in newspapers:
        random_sleep()
        issues[newspaper] = browser.get_json('http://www.faz.net/e-paper/epaper/list/%s' % newspaper)

    # Collect all issue URLs
    FAZ_urls = [issue['ausgaben'][0]['url'] for issue in issues['FAZ']]
    FAS_urls = [issue['ausgaben'][0]['url'] for issue in issues['FAS']]


    # Create output directory if it doesn't exist:
    if not os.path.isdir(args.output_directory):
        os.makedirs(args.output_directory)

    # Download all newspaper issues:
    random_sleep()
    for url in FAZ_urls + FAS_urls:
        overview = browser.get_json('http://www.faz.net/e-paper/epaper/overview/'+url)
        filename = overview['ausgabePdf']
        pdf_url = 'http://www.faz.net/e-paper/epaper/pdf/{}/{}'.format(url, filename)
        fullpath = os.path.join(args.output_directory, filename)
        if os.path.exists(fullpath):
            logging.info("{} already downloaded... ".format(filename))
            continue
        logging.info("Downloading {}...".format(filename))
        pdf = browser.get(pdf_url, stream=True)
        with open(fullpath, 'wb') as f:
            for chunk in pdf.iter_content(1024):
                f.write(chunk)
        random_sleep()

    browser.close()

class Browser(object):
    def __init__(self, user_agent, cookie_file, store_any_cookie=False):
        self.s = requests.Session()
        self.store_any_cookie = store_any_cookie
        self.cookie_file = cookie_file
        if cookie_file:
            self.s.cookies = http.cookiejar.LWPCookieJar()
            try:
                self.s.cookies.load(cookie_file, ignore_discard=self.store_any_cookie)
            except FileNotFoundError:
                pass
        headers = {
          'User-Agent': user_agent,
          'Dnt': '1',
          'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
          'Accept-Encoding': "gzip, deflate",
          'Accept-Language': "en,en-gb;q=0.8,en-us;q=0.5,de;q=0.3"
        }
        self.s.headers.update(headers)
        self.last = None

    def close(self):
        logging.debug("saving cookies")
        try:
            self.s.cookies.save(self.cookie_file, ignore_discard=self.store_any_cookie)
        except:
            pass

    def get_json(self, *args, **kwargs):
        # Different headers for json requests:
        headers = {
          'Accept': 'application/json, text/javascript, */*; q=0.01',
          'X-Requested-With': 'XMLHttpRequest',
          'Referer': 'http://www.faz.net/e-paper/',
          'Connection': 'keep-alive',
        }
        try:
            kwargs['headers'].update(headers)
        except KeyError:
            kwargs['headers'] = headers
        return self.s.get(*args, **kwargs).json()

    def set_referer(self, func, *args, **kwargs):

        if self.last:
            headers = { 'Referer': self.last }
            try:
                kwargs['headers'].update(headers)
            except KeyError:
                kwargs['headers'] = headers
        self.last = args[0]
        return func(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.set_referer(self.s.get, *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.set_referer(self.s.post, *args, **kwargs)

def random_sleep(min_sec=0.6, max_sec=5.3):
    st = random.uniform(min_sec, max_sec)
    logging.debug('Sleep time: {}'.format(st))
    time.sleep(st)

if __name__ == "__main__":
    main()

