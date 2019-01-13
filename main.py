#!/usr/bin/env python

from requests_html import HTMLSession

from parsers import WilliamsonCountyParser


KEYWORDS = ['band', 'music']
SCHOOL_LOOKUP = {
    # 'maury': (
    #     MauryCountyParser,
    #     '',
    # ),
    'williamson': (
        WilliamsonCountyParser,
        'https://selfservice.wcs.edu/MSS/employmentopportunities/default.aspx',
    ),
}


def main() -> int:
    session = HTMLSession()
    num_results = 0

    for county, (parser_class, url) in SCHOOL_LOOKUP.items():
        print(f'Fetching HTML for {county.title()} County: {url}')
        parser = parser_class(keywords=KEYWORDS)
        response = session.get(url)
        openings = parser(response.html)

        for opening in openings:
            print('-' * 30)
            print(opening)
            num_results += 1
        print()

    return num_results == 0


if __name__ == '__main__':
    exit(main())
