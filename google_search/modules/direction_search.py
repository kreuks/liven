from bs4 import BeautifulSoup

from utils import _get_search_url, get_direction_html


def direction(query, lang='en'):
    result = {}
    url = _get_search_url(query, lang=lang)
    html = get_direction_html(url)
    soup = (BeautifulSoup(html, 'html.parser')
            if html else BeautifulSoup('<html></html>', 'html.parser'))
    names = soup.findAll('div', attrs={'class': '_hw card-section'})
    link = soup.findAll('div', attrs={'class': 'rrm'})
    if names:
        names = names[0].findAll('div', attrs={'class': 'ellip'})
        result['origin'] = names[0].text.strip().replace('From ', '')
        result['destination'] = names[1].text.strip().replace('To ', '')
    paths = []
    for x in soup.findAll('div', attrs={'class': '_fk _Ij single-line'}):
        paths.append(x.text.strip().encode('ASCII', 'replace'))
    result['directions'] = paths
    result['link'] = '' if link == [] else 'https://www.google.com' + link[0].find('a')['href']
    return result
