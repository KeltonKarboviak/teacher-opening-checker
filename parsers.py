import operator
from typing import Iterable, List

import requests_html


class CountyParserMeta(type):
    def __new__(metacls, name, bases, class_dict):
        if bases != (object,):
            for attr in ['county_name', 'find_selector', 'text_getter']:
                if attr not in class_dict:
                    raise ValueError(f'Class must have a "{attr}" attribute.')
        return super().__new__(metacls, name, bases, class_dict)


class CountyParserBase(object, metaclass=CountyParserMeta):
    def __call__(self, html_element: requests_html.HTML) -> Iterable[str]:
        raise NotImplementedError('Needs concrete implementation.')


class WilliamsonCountyParser(CountyParserBase):
    county_name: str = 'williamson'
    find_selector: str = 'table.employmentopportunity'
    text_getter = operator.attrgetter('text')

    def __init__(self, keywords: List[str]):
        self.keywords = keywords

    def __call__(self, html_element: requests_html.HTML) -> Iterable[str]:
        opening_elements = html_element.find(
            self.find_selector, containing=self.keywords
        )
        return map(self.text_getter, opening_elements)
