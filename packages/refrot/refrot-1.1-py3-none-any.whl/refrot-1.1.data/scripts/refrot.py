#!python
import argparse

import requests
import lxml.html

parser = argparse.ArgumentParser('Check links for URL')
parser.add_argument(dest='url')
parser.add_argument('--ignore-external-links', '-i',
                    action='store_true',
                    help='ignore external links')
parser.add_argument('--user-agent', '-u',
                    help='User agant')


def check():
    checked, errors = get_links(args.url)
    print(f'\nLinks checked: {len(checked)}. Errors found: {len(errors)}.')
    for key in errors:
        print(errors[key], key)


def get_links(url, checked=[], errors={}):
    """Recursively check links found at url."""
    if url in checked:
        return
    if args.ignore_external_links and not url.startswith(args.url):
        return
    checked.append(url)
    try:
        if args.user_agent:
            headers = {'user-agent': args.user_agent}
            r = requests.get(url, headers=headers)
        else:
            r = requests.get(url)
        if r.history:
            status_code = r.history[0].status_code
            reason = r.history[0].reason
            print(status_code, url)
            # Ignore temporary redirects.
            if status_code != 302:
                errors[url] = f'{status_code} {reason}'
        else:
            print(r.status_code, url)
        if r.status_code != 200:
            errors[url] = f'{r.status_code} {r.reason}'
    except requests.exceptions.SSLError:
        print('SSL Cert Fail', url)
        errors[url] = 'SSL Cert Fail'
        return checked, errors
    except requests.exceptions.ConnectionError:
        print('Connection error', url)
        errors[url] = 'Connection error'
        return checked, errors

    # Don't spider external links. They can check their own pages!
    if not url.startswith(args.url):
        return
    doc = lxml.html.fromstring(r.content)
    doc.make_links_absolute(url)
    links = []
    for link in doc.xpath('//a/@href'):
        if '#' in link or 'mailto:' in link:
            continue
        if link in checked:
            continue
        links.append(link)
    for link in links:
        get_links(link, checked, errors)
    return checked, errors


if __name__ == "__main__":
    args = parser.parse_args()
    check()

