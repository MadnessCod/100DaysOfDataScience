from typing import Iterator


import scrapy
from scrapy.http import Request, Response


class MovieSeries(scrapy.Spider):
    """
    A simple scrapy class to scrape top 250 movies and series from IMDB
    """

    name = 'items'

    def start_requests(self) -> Iterator[Request]:
        """
        standard start_requests which sends Request objects to parse
        """

        urls = ['https://www.imdb.com/chart/top/?ref_=nv_mv_250',
                'https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250',]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: Response) -> Iterator[Request]:
        """
        parses urls from top 250 movies and series
        calls parse_detail function for further processing
        :param response: The HTTP response received from the request
        :return: An Iterator of scrapy Request objects
        """
        items = response.css('#__next > main > div > div.ipc-page-content-container.'
                             'ipc-page-content-container--center > section > div >'
                             'div.ipc-page-grid.ipc-page-grid--bias-left > div >'
                             'ul > li > div > div > div > div > div.sc-d5ea4b9d-0.'
                             'ejavrk.cli-children > div.ipc-title.ipc-title--base.'
                             'ipc-title--title.ipc-title-link-no-icon.ipc-title--on'
                             '-textPrimary.sc-3713cfda-2.fSzZES.cli-title.with-margin '
                             '> a::attr(href)').getall()

        for item in items:
            yield response.follow(item, callback=self.parse_detail)

    def parse_detail(self, response: Response):
        """
        Parses movies and series from url
        :param response: HTTP response received from the request
        """
        pass
