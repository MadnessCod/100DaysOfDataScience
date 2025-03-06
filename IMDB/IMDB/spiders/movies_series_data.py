from typing import Iterator


import scrapy
from scrapy.http import Request, Response


class MovieSeries(scrapy.Spider):
    """
    A simple scrapy class to scrape top 250 movies and series from IMDB
    """

    name = "items"

    def start_requests(self) -> Iterator[Request]:
        """
        standard start_requests which sends Request objects to parse
        """

        url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
        yield scrapy.Request(url=url, callback=self.parse, meta={'playwright': True})

    def parse(self, response: Response, **kwargs) -> Iterator[Request]:
        """
        parses urls from top 250 movies and series
        calls parse_detail function for further processing
        :param response: The HTTP response received from the request
        :return: An Iterator of scrapy Request objects
        """
        items = response.css(
            "#__next > main > div > div.ipc-page-content-container."
            "ipc-page-content-container--center > section > div >"
            "div.ipc-page-grid.ipc-page-grid--bias-left > div >"
            "ul > li > div > div > div > div > div.sc-d5ea4b9d-0."
            "ejavrk.cli-children > div.ipc-title.ipc-title--base."
            "ipc-title--title.ipc-title-link-no-icon.ipc-title--on"
            "-textPrimary.sc-3713cfda-2.fSzZES.cli-title.with-margin "
            "> a::attr(href)"
        ).getall()

        for item in items:
            yield response.follow(item, callback=self.parse_detail)
            break

    def parse_detail(self, response: Response):
        """
        Parses movies and series from url
        :param response: HTTP response received from the request
        """
        title = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section'
            "/section/div[2]/div[1]/h1/span/text()"
        ).get()
        rating = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/'
            "section/section/div[2]/div[2]/div/div[1]/a/"
            "span/div/div[2]/div[1]/span[1]/text()"
        ).get()
        popularity = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section'
            "/div[3]/section/section/div[2]/div[2]/div/div[3]"
            "/a/span/div/div[2]/div[1]/text()"
        ).get()
        year = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/'
            "section/section/div[2]/div[1]/ul/li[1]/a/text()"
        ).get()

        meta_score = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/'
            "div[3]/section/section/div[3]/div[2]/div[2]/ul/"
            "li[3]/a/span/span[1]/span/text()"
        ).get()
        tags = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/'
            "section/section/div[3]/div[2]/div[1]/section/div[1]/"
            "div[2]/a/span/text()"
        ).getall()
        budget = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/div/section/div/'
            "div[1]/section[12]/div[2]/ul/li[1]/div/ul/li/span/text()"
        ).get()
        first_us_ca = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/div/section/'
            "div/div[1]/section[12]/div[2]/ul/li[3]/div/ul/li[1]/"
            "span/text()"
        ).get()
        yield {
            "title": title,
            "rating": rating,
            "popularity": popularity,
            "year": year,
            "meta_score": meta_score,
            "tags": tags,
            "budget": budget,
            "first_us_ca": first_us_ca,
        }
