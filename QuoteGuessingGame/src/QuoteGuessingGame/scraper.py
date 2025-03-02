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

    async def scrape(self):
        """
        :return:
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.url)
                response.raise_for_status()
            except httpx.HTTPStatusError:
                return None
        return response.text


if __name__ == '__main__':
    quotes = QuoteScraper()
    asyncio.run(quotes.scrape())
