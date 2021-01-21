import requests
from bs4 import BeautifulSoup


def get_authors(text):
    return text.split('- ')[0]


def get_journal(text):
    return text.split('- ')[1]


def as_html(authors, title, journal, link):
    # format title
    while (1):
        if (title[0:5].lower() == '[pdf]'):
            title = title[5:]
        elif (title[0:6].lower() == '[html]'):
            title = title[6:]
        else:
            break

    # format as html string
    return '<li>{}.  <span class="title">{}.</span>  {}.  <a href="{}">View Details</a>\n'.format(authors[:-1], title, journal, link)


def write_html(output, item):
    authors = get_authors(item.select('.gs_a')[0].get_text())
    title = item.select('h3')[0].get_text()
    journal = get_journal(item.select('.gs_a')[0].get_text())
    link = item.select('a')[0]['href']
    output.write(as_html(authors, title, journal, link))


def page(url, output):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)\
            AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}
    response = requests.get(url, headers=headers)
    print(response.text)
    soup = BeautifulSoup(response.content, 'lxml')
    empty = False
    for item in soup.select('[data-lid]'):
        empty = True
        write_html(output, item)
    return empty


if __name__ == '__main__':
    base = 'https://scholar.google.com/scholar?start='
    end = '&hl=en&as_sdt=0,33&sciodt=0,33&cites=7597625062469494917&scipsc='
    f = open('bib.txt', 'w')
    start = 0
    url = base + str(start) + end
    page(url, f)
    while (page(url, f)):
        start += 10
        url = base + str(start) + end
    f.close()
