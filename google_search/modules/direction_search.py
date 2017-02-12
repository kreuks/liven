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

    li = soup.findAll('div', attrs={'class': '_s2'})
    result['flight_available'] = True if li else False

    result['flight_direction'] = direction_flight(li=li) if result['flight_available'] else None

    result['link'] = 'https://www.google.com' + link[0].find('a')['href'] if link else ''

    return result


def direction_flight(query=None, li=None):
    result = {}
    flights = check_link(li, query)
    flight_direction = []
    for flight in flights:
        link = flight.find('a')['href'] if flight.find('a') else flight['href']
        flight = re.sub(r'\b[ ]{2,}\b', '\t\t', flight.text.strip())
        flight_direction.append('<a href=\'{}\'>{}</a> \n'.format(link, flight))
    result['flight_direction'] = flight_direction
    return result


def check_link(li=None, query=None, lang='en'):
    if li:
        return (
            li[0].findAll('div', attrs={'class': '_Xnb _QJ _Z9b'})
            + li[0].findAll('div', attrs={'class': '_Xnb _QJ'})
        )
    else:
        url = get_search_url(query, lang=lang)
        html = get_direction_html(url)
        li_result = (
            BeautifulSoup(html, 'html.parser')
            if html else BeautifulSoup('<html></html>', 'html.parser')
        )

        li = li_result.findAll('div', attrs={'class': '_s2'})

        return (
            [li_result.find('h3', attrs={'class': 'r'}).find('a')]
            + li[0].findAll('div', attrs={'class': '_Xnb _QJ _Z9b'})
            + li[0].findAll('div', attrs={'class': '_Xnb _QJ'})
        )