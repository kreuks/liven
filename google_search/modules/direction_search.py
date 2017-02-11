import re

from bs4 import BeautifulSoup

from utils import get_search_url, get_direction_html


def direction(query, lang='en'):
    result = {}
    url = get_search_url(query, lang=lang)
    html = get_direction_html(url)
    soup = (BeautifulSoup(html, 'html.parser')
            if html else BeautifulSoup('<html></html>', 'html.parser'))
    names = soup.findAll('div', attrs={'class': '_hw card-section'})
    link = soup.findAll('div', attrs={'class': 'rrm'})
    if names:
        names = names[0].findAll('div', attrs={'class': 'ellip'})
        result['origin'] = names[0].text.strip()
        result['destination'] = names[1].text.strip()
    paths = []
    for x in soup.findAll('div', attrs={'class': '_fk _Ij single-line'}):
        paths.append(x.text.strip())
    result['directions'] = paths

    result['flight_direction'] = True if soup.findAll('div', attrs={'class': '_s2'}) else False

    result['link'] = 'https://www.google.com' + link[0].find('a')['href'] if link else ''
    return result


def direction_flight(li):
    res = li[0].findAll('div', attrs={'class': '_Xnb _QJ _Z9b'}) + \
          li[0].findAll('div', attrs={'class': '_Xnb _QJ'})
    for x in res:
        link = x.find('a')['href']
        flight = re.sub(r'\b[ ]{2,}\b', '\t\t', x.text.strip())
        print flight
        print '<a href=\'{}\'>{}</a>'.format(link, flight)
        # try:
        #     print x.find('div', attrs={'class': '_Xnb _QJ'}).text.strip()
        # except:
        #     print x.find('div', attrs={'class': '_Xnb _QJ _Z9b'}).text.strip()
    pass