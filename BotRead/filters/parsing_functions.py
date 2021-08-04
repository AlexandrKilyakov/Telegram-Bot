import requests
from bs4 import BeautifulSoup
import re
import asyncio
import concurrent.futures

async def run_blocking_io(func, *args):
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, func, *args)
        return result.text
# ===========================================================================================
# Работа с ссылками для парсинга
# ===========================================================================================
async def get_link_chapter(link):
	responce = await run_blocking_io(requests.get, link)
	soup = BeautifulSoup(responce, 'lxml')
	name = re.findall(r'^(.*:)//([A-Za-z0-9\-\.]+)(:[0-9]+)?(.*)$', link)[0][1].split('.')[0]

	try:
		if name == 'mangapoisk':
			block = soup.find('div', class_ = 'post-info')
			status = block.find_all('span')[2].text.split(':  ')[1].replace(' ', '')
			if status != 'Завершена':
				return soup.find_all('h2', class_ = 'h-6')[2].text.split(' ')[3]

		elif name == 'remanga':
			status = soup.find('a', class_ = 'c62').text#[Продолжается]

			if(status != '[Закончен]'):
				return soup.find_all('span', class_ = 'MuiTab-wrapper')[1].text.split(' ')[1]

		elif name == 'desu':
			status = soup.find_all('span', class_ = 'b-anime_status_tag')[1].text
			if(status != 'завершён'):
				return soup.find('a', class_ = 'b-link_button dark read-ch-online anime-date Tooltip').text.split(' ')[3]

		elif name == 'ranobelib':
			chapter = soup.find_all('div', class_ = 'info-list__row')[4]
			status = chapter.find('span').text
			if(status != 'Завершен'):
				block = soup.find('div', class_ = 'chapter-item__name')
				return block.find('a').text.replace('\n', '').split(' ')[14]

		elif name == 'ranobes':
			status = soup.find_all('span', class_ = 'grey')[2].text
			if(status != 'Завершен'):
				return soup.find('span', class_ = 'title ellipses').text.split(' ')[1]

		elif name == 'ranobehub':
			status = soup.find_all('div', class_ = 'book-meta-value')[2].text.replace('\n', '')
			if(status != 'Завершено'):
				block = soup.find('div', class_ = 'book-meta-value book-stats')
				return block.find('strong').text

		return False
	except:
		return False