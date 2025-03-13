import asyncio

from dataclasses import dataclass
from typing import Literal

import httpx


@dataclass
class QuoteScraper:
    """
    Class is used to scrapy quotes from http://quotes.toscrape.com/
    :param url: Literal http://quotes.toscrape.com/
    :type url: str
    """
    file : Literal['Quotes.json'] = 'Quotes.json'
    url : Literal['http://quotes.toscrape.com/'] = 'http://quotes.toscrape.com/'

    async def scrape(self, url) -> httpx.Response.text:
        """
        send request to url
        :param url: url to scrape
        :type url: str
        :return: httpx.Response.text
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
            text = await self.scrape(url=f'{self.url}page/{counter}/')
            if text is None:
                break


if __name__ == '__main__':
    quotes = QuoteScraper()
    asyncio.run(quotes.increment_page())
