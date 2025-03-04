import asyncio
from dataclasses import dataclass
from typing import Literal


import httpx


@dataclass
class QuoteScraper:
    """
    """
    file : Literal['Quotes.json'] = 'Quotes.json'
    url : Literal['https://quotes.toscrape.com/'] = 'https://quotes.toscrape.com/'

    async def scrape(self, url) -> httpx.Response.text:
        """
        :return:
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
        """
        counter = 1
        while True:
            text = await self.scrape(url=f'{self.url}page/{counter}')
            if text is None:
                break


if __name__ == '__main__':
    quotes = QuoteScraper()
    asyncio.run(quotes.increment_page())
