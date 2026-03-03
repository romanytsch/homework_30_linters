import aiohttp
import asyncio
from bs4 import BeautifulSoup
import urllib.parse
from typing import Set


async def fetch(session, url):
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.text()
    except:
        pass
    return None


def get_external_links(html, base_domain):
    if not html:
        return []
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        parsed = urllib.parse.urlparse(href if href.startswith('http') else urllib.parse.urljoin(base_domain, href))
        if parsed.scheme in ('http', 'https') and parsed.netloc != base_domain:
            links.append(f"{parsed.scheme}://{parsed.netloc}{parsed.path}")
    return links


async def crawl(session, url, depth, max_depth, visited, all_links):
    if depth > max_depth or url in visited:
        return

    visited.add(url)
    all_links.add(url)

    html = await fetch(session, url)
    if not html:
        return

    domain = urllib.parse.urlparse(url).netloc
    new_links = get_external_links(html, domain)

    # Асинхронно краулим новые ссылки
    tasks = [crawl(session, link, depth + 1, max_depth, visited, all_links) for link in new_links]
    if tasks:
        await asyncio.gather(*tasks)


async def main(start_urls, max_depth=3):
    async with aiohttp.ClientSession() as session:
        all_links = set()
        visited = set()

        # Краулим все стартовые URL
        tasks = [crawl(session, url, 0, max_depth, visited, all_links) for url in start_urls]
        await asyncio.gather(*tasks)

        # Сохраняем в файл
        with open('links.txt', 'w') as f:
            for link in sorted(all_links):
                f.write(link + '\n')
        print(f"Найдено {len(all_links)} ссылок в links.txt")


if __name__ == "__main__":
    urls = ['https://example.com']
    asyncio.run(main(urls))
