from typing import Iterator


import scrapy
from scrapy.http import Request, Response
from scrapy.selector import Selector


class MovieSeries(scrapy.Spider):
    """
    A simple scrapy class to scrape top 250 movies and series from IMDB
    """

    name = "items"

    def start_requests(self) -> Iterator[Request]:
        """
        standard start_requests which sends Request objects to parse
        """

        urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250",
                "https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"]
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={"playwright": True, "playwright_include_page": True},
            )

    async def parse(self, response: Response, **kwargs) -> Iterator[Request]:
        """
        parses urls from top 250 movies and series
        calls parse_detail function for further processing
        :param response: The HTTP response received from the request
        :return: An Iterator of scrapy Request objects
        """
        page = response.meta["playwright_page"]
        page.set_default_timeout(1000)
        await page.wait_for_timeout(5000)
        try:
            last_position = await page.evaluate("window.scrollY")
            while True:
                await page.evaluate("window.scrollBy(0,2000)")
                await page.wait_for_timeout(700)
                current_position = await page.evaluate("window.scrollY")
                if current_position == last_position:
                    print("Reached the bottom of the page.")
                    break
                last_position = current_position
        except AttributeError as e:
            print(f"Error: {e}")

        content = await page.content()
        selector = Selector(text=content)
        items = selector.xpath(
            '//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li/'
            'div/div/div/div/div[2]/div[1]/a/@href').getall()
        for item in items:
            yield response.follow(item, callback=self.parse_detail)

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
