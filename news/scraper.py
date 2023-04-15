from asgiref.sync import sync_to_async
from parsel import Selector
import asyncio
import httpx

from server.settings import DEFAULT_HEADERS
from news.models import News


class NewsScraper:
    MAIN_URL = "https://www.prnewswire.com/news-releases/news-releases-list/?page={}&pagesize=100"
    NEWS_LINK_XPATH = '//a[@class="newsreleaseconsolidatelink display-outline w-100"]/@href'

    def __init__(self):
        pass

    async def get_url(self, client, url):
        response = await client.get(url)
        await self.parse_links(response.text)
        return response

    async def parse_data(self):
        async with httpx.AsyncClient(headers=DEFAULT_HEADERS) as client:
            tasks = []
            for page in range(1, 20):
                print(self.MAIN_URL.format(page))
                tasks.append(asyncio.create_task(self.get_url(client, self.MAIN_URL.format(page))))
            news_gather = await asyncio.gather(*tasks)
            await client.aclose()

    async def parse_links(self, content):
        tree = Selector(text=content)
        urls = tree.xpath(self.NEWS_LINK_XPATH).extract()
        print(f'url: {urls}')
        print(f'len_url: {(len(urls))}')
        await self.save_data(urls)

    @sync_to_async
    def save_data(self, urls):
        News.objects.bulk_create([News(**{'link': url}) for url in urls])

    async def main(self):
        await self.parse_data()


if __name__ == "__main__":
    scraper = NewsScraper()
    asyncio.run(scraper.main())
