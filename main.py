#!/usr/bin/env python

import json

from requests_html import HTMLSession

from parsers import MauryCountyParser, WilliamsonCountyParser


KEYWORDS = ['band', 'choir', 'chorus', 'music']
SCHOOL_LOOKUP = {
    'maury': (
        MauryCountyParser,
        'https://ats4.searchsoft.net/ats/job_board?APPLICANT_TYPE_ID=00000001&COMPANY_ID=MA000230',
    ),
    'williamson': (
        WilliamsonCountyParser,
        'https://selfservice.wcs.edu/MSS/employmentopportunities/default.aspx',
    ),
}


def main() -> int:
    session = HTMLSession()
    num_results = 0

    print(f'Keywords = {json.dumps(KEYWORDS)}')

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
