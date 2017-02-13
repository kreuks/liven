from __future__ import unicode_literals

from utils import get_search_url, get_html
from bs4 import BeautifulSoup
import urlparse
from urllib2 import unquote
from unidecode import unidecode
from re import match
from copy import deepcopy


class GoogleResult:

    """Represents a google search result."""

    def __init__(self):
        self.name = None  # The title of the link
        self.link = None  # The external link
        self.google_link = None  # The google link
        self.description = None  # The description of the link
        self.thumb = None  # Thumbnail link of website (NOT implemented yet)
        self.cached = None  # Cached version link of page
        self.page = None  # Results page this one was on
        self.index = None  # What index on this page it was on

    def __repr__(self):
        name = self._limit_str_size(self.name, 55)
        description = self._limit_str_size(self.description, 49)

        list_google = ["GoogleResult(",
                       "name={}".format(name), "\n", " " * 13,
                       "description={}".format(description)]

        return "".join(list_google)

    def _limit_str_size(self, str_element, size_limit):
        """Limit the characters of the string, adding .. at the end."""
        if not str_element:
            return None

        elif len(str_element) > size_limit:
            return unidecode(str_element[:size_limit]) + ".."

        else:
            return unidecode(str_element)


# PUBLIC
def search(query, pages=1, lang='en', void=True):
    """Returns a list of GoogleResult.

    Args:
        query: String to search in google.
        pages: Number of pages where results must be taken.

    Returns:
        A GoogleResult object."""

    results = []
    complete_description = {}
    for i in range(pages):
        url = get_search_url(query, i, lang=lang)
        html = get_html(url)

        if html:
            soup = BeautifulSoup(html, "html.parser")
            divs = deepcopy(soup.findAll("div", attrs={"class": "g"}))
            complete_desc = deepcopy(soup.findAll("div", attrs={"class": "_o0d"}))

            if complete_desc:
                complete_description['name'] = _complete_name(complete_desc)
                complete_description['tag'] = _complete_tag(complete_desc)
                complete_description['description'] = _complete_desc(complete_desc)
                complete_description['born'] = _complete_born(complete_desc)
                complete_description['image'] = _complete_image(soup)
                complete_description['complete'] = _complete_description(complete_desc)

            j = 0
            for li in divs:
                res = GoogleResult()

                res.page = i
                res.index = j

                res.name = _get_name(li)
                res.link = _get_link(li)
                res.google_link = _get_google_link(li)
                res.description = _get_description(li)
                res.thumb = _get_thumb()
                res.cached = _get_cached(li)
                if void is True:
                    if res.description is None:
                        continue
                results.append(res)
                j += 1

    return results, complete_description


def _complete_name(li):
    try:
        result = li[0].find("div", attrs={"class": "_B5d"})
        if result:
            return result.text.strip()
    except KeyError:
        return None


def _complete_tag(li):
    try:
        result = li[0].find("div", attrs={"class": "_zdb _Pxg"})
        if result:
            return result.text.strip()
    except KeyError:
        return None


def _complete_desc(li):
    try:
        return li[1].text.strip().encode('ASCII', 'replace').replace('Wikipedia', '')
    except KeyError:
        return None


def _complete_born(li):
    try:
        return li[3].text.strip().replace("Born: ", "").encode('ASCII', 'replace')
    except KeyError:
        return None


def _complete_image(li):
    try:
        image_link = li.findAll("div", attrs={"class": "_x8d"})[0].find("img")["src"]
        return None if image_link.startswith('/') else image_link
    except (TypeError, IndexError):
        return None


def _complete_description(li):
    name = _complete_name(li)
    review_result = li[2].find('div', attrs={'class': '_POh'})
    if name and review_result:
        result = name + '\n'
        for row in li[3:-1]:
            row = row.text.strip().replace('Wikipedia', '')
            if row == 'PetunjukSitus Web':
                continue
            result = result + '\n' + row
        return result
    elif name and not review_result:
        result = name + '\n'
        for row in li[1:]:
            row = row.text.strip().replace('Wikipedia', '')
            if row == 'PetunjukSitus Web':
                continue
            result = result + '\n' + row
        return result
    else:
        return None


def _get_name(li):
    """Return the name of a google search."""
    a = li.find("a")
    # return a.text.encode("utf-8").strip()
    if a is not None:
        return a.text.strip()
    return None


def _get_link(li):
    """Return external link from a search."""
    try:
        a = li.find("a")
        link = a["href"]
    except:
        return None

    if link.startswith("/url?"):
        m = match('/url\?(url|q)=(.+?)&', link)
        if m and len(m.groups()) == 2:
            return unquote(m.group(2))

    return None


def _get_google_link(li):
    """Return google link from a search."""
    try:
        a = li.find("a")
        link = a["href"]
    except:
        return None

    if link.startswith("/url?") or link.startswith("/search?"):
        return urlparse.urljoin("http://www.google.com", link)

    else:
        return None


def _get_description(li):
    """Return the description of a google search.

    TODO: There are some text encoding problems to resolve."""

    sdiv = li.find("div", attrs={"class": "s"})
    if sdiv:
        stspan = sdiv.find("span", attrs={"class": "st"})
        if stspan is not None:
            # return stspan.text.encode("utf-8").strip()
            return stspan.text.strip()
    else:
        return None


def _get_thumb():
    """Return the link to a thumbnail of the website."""
    pass


def _get_cached(li):
    """Return a link to the cached version of the page."""
    links = li.find_all("a")
    if len(links) > 1 and links[1].text == "Cached":
        link = links[1]["href"]
        if link.startswith("/url?") or link.startswith("/search?"):
            return urlparse.urljoin("http://www.google.co.id", link)
    return None
