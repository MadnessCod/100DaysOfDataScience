import asyncio

from dataclasses import dataclass
from typing import Literal

import httpx

from bs4 import BeautifulSoup


@dataclass
class QuoteScraper:
    """
    Class is used to scrapy quotes from http://quotes.toscrape.com/
    :param url: Literal http://quotes.toscrape.com/
    :type url: str
    """

    file: Literal["Quotes.json"] = "Quotes.json"
    url: Literal["http://quotes.toscrape.com/"] = "http://quotes.toscrape.com/"

    async def scrape(self, url) -> httpx.Response.text:
        """
        send request to url
        :param url: url to scrape
        :type url: str
        :return: html of response
        :rtype: str
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
            except httpx.HTTPStatusError:
                return None
            return response.text

    async def increment_page(self) -> None:
        """
        incrementing page number for http://quotes.toscrape.com/
        """
        counter = 1
        while True:
            text = await self.scrape(url=f"{self.url}page/{counter}/")
            if text is None:
                break
            await self.text_extract(text)
            counter += 1

    async def text_extract(self, text: str) -> None:
        """
        extracts data from each quote in each page
        :param text: text to extract data from
        :type text: str
        :return: None
        """
        soup = BeautifulSoup(text, "html.parser")
        quotes = soup.find_all("div", class_="col-md-8")[1].find_all(
            "div", class_="quote"
        )
        for quote in quotes:
            quote_text = quote.find("span", class_="text").text
            author = quote.find("small", class_="author").text
            author_link = quote.find_all("span")[1].find("a").get("href")
            tags = [a.text for a in quote.find("div", class_="tags").find_all("a")]
            tags_link = [
                a.get("href") for a in quote.find("div", class_="tags").find_all("a")
            ]


if __name__ == "__main__":
    quotes = QuoteScraper()
    asyncio.run(quotes.increment_page())
