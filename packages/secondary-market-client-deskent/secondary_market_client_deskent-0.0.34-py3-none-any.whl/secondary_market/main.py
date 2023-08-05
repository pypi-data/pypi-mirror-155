"""
Author: Deskent
"""
import asyncio
import datetime
import json
import os
import time
from typing import Any, List
import logging

import aiohttp
import aiohttp.client_exceptions
import selenium
from selenium.webdriver.common.by import By
import selenium.common
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from myloguru.my_loguru import get_logger


class SecondaryClient:
    """Client software for Secondary Market Bot

    Attributes:
        browser: instance of selenium webdriver
        auction_id: int - auction id number for cookie imitation
        product_data: list[dict] - list of products data for buying
        requests_count: int - number of requests for each product will be sent
        proxy_login: str - login for proxy access
        proxy_password: str - password for proxy access
        headers: dict - browser headers

     Methods:
         start
     """

    def __init__(
            self,
            host: str = "127.0.0.1",
            browser: Any = None,
            auction_id: int = 0,
            product_data=None,
            requests_count: int = 0,
            sale_time: datetime = None,
            proxy_login: str = '',
            proxy_password: str = '',
            currency: str = "BUSD",
            headers=None,
            check_status_id: int = -1,
            license_key: str = '',
            prepare_time: int = 30,
            debug: bool = False
    ) -> None:
        self.browser: Any = browser
        self.auction_id: int = auction_id
        self.prepare_time: int = prepare_time
        self.product_data: List[dict] = product_data
        self.requests_count: int = requests_count
        self.sale_time: datetime = sale_time
        self.proxy_login: str = proxy_login
        self.proxy_password: str = proxy_password
        self.currency: str = currency
        self.headers: dict = headers
        self.check_status_id: int = -check_status_id
        self.license_key: str = license_key
        self.place_a_bid_button: str = '//button[@class=" css-1gv20g8"]'
        self.confirm_a_bid_button: str = '//button[@class=" css-1yciwke"]'
        self.accept_cookie_button_x_path: str = '//*[@id="onetrust-accept-btn-handler"]'
        self.term_accepted: bool = False
        self.request_id: int = 0
        self._server_url: str = f"http://{host}/api/v1"
        self._license_check_url: str = self._server_url + '/license/check_license'
        self._license_approve_url: str = self._server_url + '/license/license_approve'
        self._work_url: str = self._server_url + '/product/secondary_market'
        self.license_file_name: str = 'license'
        self.DEBUG: bool = debug

    async def start(self) -> None:
        """Main class function"""

        if not self.DEBUG:
            if not await self._check_license_key():
                return
            if not await self._get_license_approve():
                return

        self._logging_in()
        self._imitation_cookie()
        self._wait_for_time()
        self._get_headers()
        if await self._buy_products():
            logger.success("Request sent. Results will be sent to Telegram.")
            return
        logger.warning("Request sent with errors.")

    async def _check_license_key(self) -> bool:
        """Checks license key"""

        logger.info("Checking license key...")

        self.license_key: str = self._load_license_key()
        if not self.license_key:
            logger.error(f"License not found.")
            return False
        data: dict = {
            "license_key": self.license_key
        }
        answer: dict = await self._send_request(url=self._license_check_url, data=data)
        if not answer:
            logger.error(f"\n\tNo answer from checking license: "
                         f"\n\tLicense key: [{self.license_key}]")
            return False
        success: bool = answer.get("success")
        text: str = answer.get("message")
        logger.info(f"Checking license key: {text}")
        self.check_status_id: int = answer.get("data", {}).get("check_status_id", -1)
        self.status: int = answer.get("data", {}).get("status", -1)

        return success

    async def _get_license_approve(self) -> bool:
        """Returns license approved result"""

        logger.info("Getting license approve...")
        logger.success("\n\n\n\t\tПодтвердите запрос в телеграм-боте и нажмите Enter:\n\n")
        input()
        logger.info("License approving...")
        if await self.__get_license_approve():
            logger.info("License approve: OK")
            return True
        logger.warning(f"License {self.license_key} approve: FAIL")
        return False

    def _logging_in(self) -> None:
        """Wait for user logging in"""

        logger.info('Logging in...')
        self.browser.maximize_window()
        self.browser.get("https://binance.com/ru/nft")
        self._time_sleep(3)
        self._click_to_button(self.accept_cookie_button_x_path)
        self._time_sleep(1)
        log_in_button: str = '//*[@id="header_login"]'
        self._click_to_button(log_in_button)

        logger.success('\n\n\n\t\tLog in Binance account and press ENTER:\n\n')
        input()
        logger.debug('Logging in...')

    def _imitation_cookie(self) -> None:
        """Получение кукисов (прогрев)"""

        logger.info('Simulation of human work for Binance')
        self.browser.get(f'https://www.binance.com/en/nft/balance?tab=nft')
        self._time_sleep(5)
        self.browser.get('https://www.binance.com/ru/nft/home')
        self._press_accept_button()
        self._time_sleep(5)
        self._press_accept_button()
        self._time_sleep(10)
        self.browser.get(
            f'https://www.binance.com/ru/nft/goods/blindBox'
            + f'/detail?productId={self.auction_id}&isOpen=true&isProduct=1'
        )

    def _wait_for_time(self) -> None:
        """Wait for time before prepare_time to final time"""

        stop_time: datetime = self.sale_time - datetime.timedelta(seconds=self.prepare_time)
        while datetime.datetime.utcnow() < stop_time:
            left: int = (stop_time - _get_current_time()).seconds
            logger.info(f'Start after: [{left}] seconds')
            time.sleep(1)

    def _get_headers(self) -> None:
        """Получение заголовков"""

        logger.info("Getting headers")
        self._press_pay_a_bid_button()
        self._time_sleep(3)
        url = 'https://www.binance.com/bapi/nft/v1/private/nft/nft-trade/preorder-create'
        for request in self.browser.requests:
            if str(request.url) == url:
                cookies = request.headers['cookie']
                csrftoken = request.headers['csrftoken']
                deviceinfo = 'eyJzY3JlZW5fcmVzb2x1dGlvbiI6IjE5MjAsMTA4MCIsImF2YWlsYWJsZV9zY3JlZW5' \
                             'fcmVzb2x1dGlvbiI6IjE4NTIsMTA1MyIsInN5c3RlbV92ZXJzaW9uIjoiTGludXggeD' \
                             'g2XzY0IiwiYnJhbmRfbW9kZWwiOiJ1bmtub3duIiwic3lzdGVtX2xhbmciOiJlbi1VU' \
                             'yIsInRpbWV6b25lIjoiR01UKzIiLCJ0aW1lem9uZU9mZnNldCI6LTEyMCwidXNlcl9h' \
                             'Z2VudCI6Ik1vemlsbGEvNS4wIChYMTE7IExpbnV4IHg4Nl82NCkgQXBwbGVXZWJLaXQ' \
                             'vNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzk2LjAuNDY2NC45MyBTY' \
                             'WZhcmkvNTM3LjM2IiwibGlzdF9wbHVnaW4iOiJQREYgVmlld2VyLENocm9tZSBQREYg' \
                             'Vmlld2VyLENocm9taXVtIFBERiBWaWV3ZXIsTWljcm9zb2Z0IEVkZ2UgUERGIFZpZXd' \
                             'lcixXZWJLaXQgYnVpbHQtaW4gUERGIiwiY2FudmFzX2NvZGUiOiIzMGYwZWY1YiIsIn' \
                             'dlYmdsX3ZlbmRvciI6Ikdvb2dsZSBJbmMuIChJbnRlbCkiLCJ3ZWJnbF9yZW5kZXJlc' \
                             'iI6IkFOR0xFIChJbnRlbCwgTWVzYSBJbnRlbChSKSBVSEQgR3JhcGhpY3MgNjIwIChL' \
                             'QkwgR1QyKSwgT3BlbkdMIDQuNiAoQ29yZSBQcm9maWxlKSBNZXNhIDIxLjIuMikiLCJ' \
                             'hdWRpbyI6IjEyNC4wNDM0NzUyNzUxNjA3NCIsInBsYXRmb3JtIjoiTGludXggeDg2XzY' \
                             '0Iiwid2ViX3RpbWV6b25lIjoiRXVyb3BlL0NoaXNpbmF1IiwiZGV2aWNlX25hbWUiOiJ' \
                             'DaHJvbWUgVjk2LjAuNDY2NC45MyAoTGludXgpIiwiZmluZ2VycHJpbnQiOiIyMTc5Y' \
                             'jEyNmM4N2Q0YzM3ODc3ZmM5NWFhMTIxNmRkOSIsImRldmljZV9pZCI6IiIsInJlbGF0' \
                             'ZWRfZGV2aWNlX2lkcyI6IjE2Mzk5MTA5Nzg2NjMySE8zeWExNUloV1p3a1M5ZWVCIn0='
                xNftCheckbotSitekey = request.headers['x-nft-checkbot-sitekey']
                xNftCheckbotToken = request.headers['x-nft-checkbot-token']
                xTraceId = request.headers['x-trace-id']
                xUiRequestTrace = request.headers['x-ui-request-trace']
                bnc_uuid = request.headers['bnc-uuid']
                fvideo_id = request.headers['fvideo-id']
                user_agent = request.headers['user-agent']

                self.headers = {
                    'Host': 'www.binance.com',
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'clienttype': 'web',
                    'x-nft-checkbot-token': xNftCheckbotToken,
                    'x-nft-checkbot-sitekey': xNftCheckbotSitekey,
                    'x-trace-id': xTraceId,
                    'x-ui-request-trace': xUiRequestTrace,
                    'content-type': 'application/json',
                    'cookie': cookies,
                    'csrftoken': csrftoken,
                    'device-info': deviceinfo,
                    'bnc-uuid': bnc_uuid,
                    'fvideo-id': fvideo_id,
                    'user-agent': user_agent,
                }
        logging.debug(f"\nHeaders: \n{self.headers}\n")

    async def _buy_products(self) -> bool:
        """Sends request for buying products"""

        logger.info("Send data for buying...")

        data: dict = {
            "headers": self.headers,
            "product_data": self.product_data,
            "requests_count": self.requests_count,
            "proxy_login": self.proxy_login,
            "proxy_password": self.proxy_password,
            "sale_time": str(self.sale_time),
            "currency": self.currency,
            "check_status_id": self.check_status_id
        }
        logger.debug(
            f"\nStart Lot time before sending from timestamp: {self.sale_time}"
            f"\nStart Current time: {_get_current_time()}"
            f"\nSending data: {data}")

        logger.success(f"Buying: WAITING results from server...")
        answer: dict = await self._send_request(url=self._work_url, data=data)
        logger.debug(f"Answer: {answer}")
        return answer.get("success", False)

    def _press_accept_button(self) -> None:
        if self.term_accepted:
            return
        accept_rules_button: str = '//button[text()="Accept"]'
        if not self._click_to_button(accept_rules_button):
            logger.error(f"Button not found: 'Accept'")
            accept_rules_button: str = '//button[text()="Принять"]'
            if not self._click_to_button(accept_rules_button):
                logger.error(f"Button not found: 'Принять'")
                return
            logger.success("Button found: 'Принять'")
            self.term_accepted = True
            return
        logger.success("Button found: 'Accept'")
        self.term_accepted = True

    @staticmethod
    def _time_sleep(timeout: int) -> None:
        logger.debug(f"Pause {timeout} sec")
        time.sleep(timeout)

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
    def get_current_unix_timestamp() -> float:
        return datetime.datetime.utcnow().replace(tzinfo=None).timestamp()

    def _load_license_key(self) -> str:
        """Loads and returns license key from file
        Returns empty string if file not exists"""

        if not os.path.exists(self.license_file_name):
            logger.error(f"License file not found: {self.license_file_name}")
            return ''
        with open(self.license_file_name, 'r', encoding='utf-8') as f:
            license_key: str = f.read()
        logger.debug(f"License: [{license_key}]")
        return license_key.strip()

    async def __get_license_approve(self) -> bool:
        """Returns approving license request result"""

        data: dict = {
            "license_key": self.license_key,
            "check_status_id": self.check_status_id
        }
        result: dict = await self._send_request(url=self._license_approve_url, data=data)

        return result.get('success', False)

    async def _send_request(self, url: str, data: dict) -> dict:
        """Sends post request to url with data"""

        result = {}

        proxy_data: str = f"http://{self.proxy_login}:{self.proxy_password}@{self.product_data[0].get('proxy')}/"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url=url, json=data, proxy=proxy_data) as response:
                    status: int = response.status
                    if status == 200:
                        result: dict = await response.json()
                    elif status == 204:
                        result = {"status": 204}
                    else:
                        logger.error(f"\n\t\tERROR:"
                                     f"\n\t\tStatus: {status}"
                                     f"\n\t\tData: {await response.text()}"
                        )
            except aiohttp.client_exceptions.ClientConnectorError as err:
                logger.error(
                    f"\n\tClientConnectorError:"
                    f"\n\tError text: {err}"
                )
        logger.debug(
            f"\nSending request:"
            f"\n\t\tURL: {url}"
            f"\n\t\tDATA: {data}"
            f"\n\t\tSTATUS: {status}"
            f"\n\t\tRESULT: {result}"
        )

        return result

    def _press_pay_a_bid_button(self):
        logger.info("Press 'Pay a bid' button...")
        if self._click_to_button(self.place_a_bid_button):
            logger.info("Press 'Pay a bid' button: OK")
            self._time_sleep(3)


def _get_current_time() -> 'datetime':
    return datetime.datetime.utcnow()


def _get_sale_datetime(sale_time: dict, products: int, value: int) -> 'datetime':
    if isinstance(sale_time, dict):
        spam: float = value * products
        return datetime.datetime(**sale_time) - datetime.timedelta(seconds=spam)
    raise TypeError("Sale time must be a dictionary.")


def _check_sale_time(sale_datetime: 'datetime') -> bool:
    logger.debug(f"Start Lot time: {sale_datetime}"
                 f"\nStart Current time: {_get_current_time()}")
    if sale_datetime > datetime.datetime.utcnow():
        return True
    logger.warning(f"Cannot run job in past time.")


def _update_product_data(data: List[dict]) -> List[dict]:
    for elem in data:
        elem.update(tradeType=0)
    return data


def _is_data_valid(data: List[dict]) -> List[dict]:
    if not data:
        raise ValueError("No data")
    if isinstance(data, list):
        try:
            return json.loads(json.dumps(data))
        except Exception:
            logger.error("product_data is not valid list")
            raise
    raise TypeError("product_data must be a list")


async def _check_proxies(product_data: List[dict], proxy_login: str, proxy_password: str) -> bool:
    logger.info("Checking proxies...")
    async with aiohttp.ClientSession() as session:
        proxy: str = product_data[0].get('proxy')
        proxy_data: str = f"http://{proxy_login}:{proxy_password}@{proxy}/"
        url = 'https://www.google.com/'
        try:
            async with session.get(url=url, proxy=proxy_data) as response:
                status: int = response.status
                if status == 200:
                    logger.info(f"Proxy {proxy}: OK")
                    return True
        except Exception as err:
            text = f"Proxy {proxy} doesn`t work: {err}"
            logger.error(text)


def get_browser():
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


async def main(
        auction_id: int,
        requestsNumber: int,
        product_data: List[dict],
        currency: str,
        saleTime: dict,
        proxy_login: str,
        proxy_password: str,
        host: str = '127.0.0.1',
        prepare_time: int = 0,
        debug: bool = False,
        level: int = 20,
        prepare_multiplier: int = 15,
        value: int = 1
) -> None:
    global logger
    logger = get_logger(level)
    if not await _check_proxies(product_data, proxy_login, proxy_password):
        return
    if not _is_data_valid(product_data):
        return
    product_data: List[dict] = _update_product_data(product_data)
    products_count = len(product_data)
    sale_datetime: 'datetime' = _get_sale_datetime(
        sale_time=saleTime, products=products_count, value=value)
    prepare_time += products_count * prepare_multiplier
    if not _check_sale_time(sale_datetime):
        return
    logger.debug(f"Products: {product_data}")

    browser = get_browser()
    client = SecondaryClient(
        browser=browser, auction_id=auction_id, requests_count=requestsNumber,
        product_data=product_data, currency=currency, sale_time=sale_datetime,
        proxy_login=proxy_login, proxy_password=proxy_password, host=host, prepare_time=prepare_time,
        debug=debug
    )
    await client.start()

    logger.success("\n\n\t\tPress enter to exit...")
    input()
    browser.close()


def start(*args, **kwargs):
    try:
        asyncio.new_event_loop().run_until_complete(main(*args, **kwargs))
    except (KeyboardInterrupt, selenium.common.exceptions.NoSuchWindowException):
        pass
    except selenium.common.exceptions.WebDriverException as err:
        logger.info(err)
    logger.info("End of program.")
