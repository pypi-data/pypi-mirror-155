import datetime
import json
import time
from json import JSONDecodeError
from typing import Tuple
from dataclasses import dataclass

import aiohttp
import asyncio
import logging

import selenium.common.exceptions
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from seleniumwire.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from myloguru.my_loguru import get_logger


@dataclass
class BybitClient:
    browser: Chrome
    product_data: dict
    requests_count: int
    proxies: tuple
    proxy_login: str
    proxy_password: str
    auction_id: int
    sale_time: datetime

    async def run(self):
        self._logging_in()

        product_url: str = f"https://www.bybit.com/ru-RU/nft/detail/?id={self.auction_id}"
        self.browser.get(product_url)

        if not await self._prepare_to_purchase():
            logger.error("Error purchasing")
            return

        logger.info('Trying purchase.')
        results = await self._purchase_lot()
        _save_to_json(data=results, file_name='result.json')
        logger.info("\nResults:")
        for result in results:
            logger.info(f"\n{result}")

        logger.success("Press ENTER for exit...")
        input()

    def _logging_in(self) -> None:
        """Wait for user logging in"""

        logger.info('Logging in...')
        self.browser.maximize_window()
        self.browser.get("https://www.bybit.com/ru-RU/login")
        logger.success('\n\n\n\t\tLog in your account and press ENTER:\n\n')
        input()
        logger.debug('Logging in: Done')

    def _get_headers(self):
        """Получение заголовков"""

        logger.info('Getting headers')
        self._time_sleep(1)
        url = "https://api2.bybit.com/spot/api/asset/get"
        for request in self.browser.requests:
            if str(request.url) == url:
                user_agent = request.headers['user-agent']
                logger.debug(f"user_agent: {user_agent}")
                self.headers = {
                    "authority": "api2.bybit.com",
                    "method": "POST",
                    "path": "/spot/api/nft/v1/order/buy",
                    "scheme": "https",
                    "accept": "application/json, text/plain, */*",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "ru-ru",
                    "content - length": "22",
                    'content-type': 'application/json',
                    "origin": "https://www.bybit.com",
                    "platform": "pc",
                    "referer": "https://www.bybit.com/",
                    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"98\", \"Google Chrome\";v=\"98\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "\"Windows\"",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    'usertoken': request.headers['usertoken'],
                    'user-agent': user_agent
                }
        logger.info('Getting headers: Done')
        logger.debug(f'headers: {self.headers}')
        return self.headers

    async def __create_tasks(self, session: aiohttp.ClientSession):
        """Формирование задач-запросов"""

        tasks = []
        url = "https://api2.bybit.com/spot/api/nft/v1/order/buy"
        params = {
            "url": url,
            "data": json.dumps(self.product_data),
            "ssl": False
        }
        for _ in range(self.requests_count):
            tasks.append(asyncio.create_task(session.post(**params)))

        return tasks

    async def _purchase_lot(self) -> list:
        """Отправка запросов, получение данных"""

        logger.info("Collecting requests. It will take a few seconds...")
        async with aiohttp.ClientSession(headers=self.headers) as session:
            tasks = await self.__create_tasks(session)

            responses = await asyncio.gather(*tasks)
            logger.info(f"Total received: {len(responses)}")

            return [await response.text()
                    for response in responses]

    async def _get_product_data(self) -> dict:
        """"""
        result = {}
        url: str = f"https://api2.bybit.com/spot/api/nft/v1/market/detail?id={self.auction_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                status_code = response.status
                if status_code == 200:
                    try:
                        result = await response.json()
                    except JSONDecodeError as err:
                        logger.error(f"JSON ERROR: {err}")

        return result

    async def _get_sale_time(self) -> int:
        logger.info("Getting product data.")
        data: dict = await self._get_product_data()
        logger.info("Getting product data: Done")

        return data.get("result", {}).get("addTime", 0)

    def _get_time_to_purchase(self) -> int:
        return (self.sale_time - datetime.datetime.now()).seconds

    async def _prepare_to_purchase(self) -> bool:
        time_to_purchase: int = self._get_time_to_purchase()

        while time_to_purchase > 5:
            logger.info(f"Remain {time_to_purchase} seconds")
            time.sleep(1)
            time_to_purchase: int = self._get_time_to_purchase()

        if not self._get_headers():
            logger.error("Error headers")
            return False

        time_to_purchase: int = self._get_time_to_purchase()
        logger.info("Time remains:", time_to_purchase)
        if time_to_purchase <= 0:
            logger.info("Time is up")
            return False

        while time_to_purchase > 0:
            logger.info(f"Remain {time_to_purchase} seconds")
            time.sleep(0.1)
            time_to_purchase: int = self._get_time_to_purchase()

        return True

    def _click_to_button(self, x_path: str) -> bool:
        try:
            elem = self.browser.find_element(By.XPATH, x_path)
            if not elem:
                return False
            elem.click()
            return True
        except Exception:
            logger.debug(f"Button not found: [{x_path}]")

    @staticmethod
    def _time_sleep(timeout: int) -> None:
        logger.debug(f"Pause {timeout} sec")
        time.sleep(timeout)


def _get_browser() -> Chrome:
    logging.getLogger('WDM').setLevel(logging.NOTSET)
    logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.NOTSET)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('--lang=en')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--log-level 3')
    options.add_argument('--disable-logging')
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options,
        service_log_path='/dev/null')


def _save_to_json(data, file_name: str = "default.json") -> None:
    logger.debug(f"\nData for save:\n{data}")
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def _get_current_time() -> 'datetime':
    return datetime.datetime.utcnow()


def _get_sale_datetime(sale_time: dict) -> 'datetime':
    if isinstance(sale_time, dict):
        return datetime.datetime(**sale_time)
    raise TypeError("Sale time must be a dictionary.")


def _check_sale_time(sale_datetime: 'datetime') -> bool:
    logger.debug(f"Start Lot time: {sale_datetime}"
                 f"\nStart Current time: {_get_current_time()}")
    if sale_datetime > datetime.datetime.utcnow():
        return True
    logger.warning(f"Cannot run job in past time.")


async def _check_proxy(session, proxy_data: str):
    logger.info(f"Checking proxy: {proxy_data}...")
    url = 'https://www.google.com/'
    try:
        async with session.get(url=url, proxy=proxy_data, timeout=5) as response:
            status: int = response.status
            if status == 200:
                logger.info(f"Proxy {proxy_data}: OK")
                return True
    except Exception as err:
        text = f"Proxy {proxy_data} doesn`t work: {err}"
        logger.error(text)
    return False


async def _check_proxies(proxies: Tuple[str], proxy_login: str, proxy_password: str) -> bool:
    logger.info("Checking proxies...")
    results = []
    async with aiohttp.ClientSession() as session:
        for proxy in proxies:
            proxy_data: str = f"http://{proxy_login}:{proxy_password}@{proxy}/"
            check: bool = await _check_proxy(session, proxy_data)
            results.append(check)
    return all(results)


async def main(
        auction_id: int,
        sale_time: dict,
        requests_count: int,
        proxies: Tuple[str],
        proxy_login: str,
        proxy_password: str,
        level: int = 20,
        debug: bool = False,
        host: str = ''
):
    global logger
    logger = get_logger(level)
    if not await _check_proxies(proxies, proxy_login, proxy_password):
        return
    sale_datetime: 'datetime' = _get_sale_datetime(sale_time=sale_time)
    if not _check_sale_time(sale_datetime):
        return

    product_data = {"merchandiseId": auction_id}
    browser = _get_browser()
    parser = BybitClient(
        browser=browser, product_data=product_data, requests_count=requests_count,
        sale_time=sale_datetime, proxies=proxies, proxy_login=proxy_login,
        proxy_password=proxy_password, auction_id=auction_id
    )
    await parser.run()


def start(*args, **kwargs):
    try:
        asyncio.new_event_loop().run_until_complete(main(*args, **kwargs))
    except (KeyboardInterrupt, selenium.common.exceptions.NoSuchWindowException):
        pass
    except selenium.common.exceptions.WebDriverException as err:
        logger.info(err)
    logger.info("End of program.")
