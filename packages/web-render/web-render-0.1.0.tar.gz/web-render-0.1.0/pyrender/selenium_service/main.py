"""
Copyright 2022 Andrey Plugin (9keepa@gmail.com)
Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0
https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec
https://github.com/diprajpatra/selenium-stealth
"""
import traceback
import time
import zlib
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from multiprocessing.connection import Listener
from queue import Queue
from itertools import count
from threading import Thread
from pyrender.tool import log
from pyrender.interface import MessageProtocol, IRenderData
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Type, Union
from selenium_stealth import stealth
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, \
    NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement

logger = log(__name__)


class Webbrowser:

    data: Dict[str, IRenderData] = dict()
    queue = Queue()

    @classmethod
    def make_webdriver(cls, config):
        co = Options()
        if config.PROXY_SERVER:
            co.add_argument(
                "--proxy-server={}".format(config.PROXY_SERVER))
        if config.HEADLESS:
            co.add_argument('--headless')

        co.add_argument('--disable-blink-features=AutomationControlled')
        co.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        co.add_experimental_option("excludeSwitches", ["enable-automation"])
        if config.DISABLE_IMAGE:
            chrome_prefs = {}
            chrome_prefs["profile.default_content_settings"] = {"images": 2}
            chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
            co.add_experimental_option("prefs", chrome_prefs)
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=co)
        if config.LOAD_TIMEOUT:
            driver.set_page_load_timeout(config.LOAD_TIMEOUT)
        return cls(driver, config)

    def __init__(self, driver: WebDriver, config):
        self.config = config
        self.driver = driver

        if self.config.STEALTH:
            stealth(self.driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                               '(KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36')

        if self.config.WEBDRIVER_WAIT:
            self._web_wait = WebDriverWait(
                self.driver, self.config.WEBDRIVER_WAIT,
                ignored_exceptions=StaleElementReferenceException
            )

    def web_wait(self, web_wait: dict):
        if web_wait is None:
            # no check
            return
        handler_name = web_wait['name']
        css_selectors: List[str] = web_wait['value']
        handler: Union[Type[ElementsPresenceInDOM]] = wait_handler[handler_name]
        self._web_wait.until(handler(css_selectors))

    def set_url(self, message: MessageProtocol):
        self.driver.get(message.payload['url'])
        js_data = None
        status_code = 200

        if message.payload['jscript']:
            result = self.driver.execute_script(message.payload['jscript'])
            if isinstance(result, int) or isinstance(result, str):
                js_data = result
            time.sleep(0.15)

        if message.payload['wait']:
            time.sleep(float(message.payload['wait']))

        try:
            self.web_wait(message.payload['web_wait'])
        except TimeoutException:
            status_code = 408

        Webbrowser.data[message.payload['id']] = IRenderData(
            html=IRenderData.compress_zlib(self.driver.page_source),
            expiration_date=message.payload['expiration_date'],
            status_code=status_code,
            javascript=js_data
        )

    def work_service(self):
        for _ in count():
            message = self.queue.get()
            try:
                self.set_url(message)
                logger.info(f"message {message}")
            except Exception as e:
                logger.error(f"Error {e}", exc_info=True)

    def get_content_active_page(self, message: MessageProtocol) -> bytes:
        js_data = None

        if message.payload['jscript']:
            result = self.driver.execute_script(message.payload['jscript'])
            if isinstance(result, int) or isinstance(result, str):
                js_data = result

        if message.payload['wait']:
            time.sleep(float(message.payload['wait']))

        render_data = IRenderData(
            html=zlib.compress(self.driver.page_source.encode("utf8")),
            expiration_date=0,
            javascript=js_data,
            status_code=200
        )

        return render_data.pickle_dump()

    def clear_service(self):
        for _ in count():
            for k in list(Webbrowser.data.keys()):
                if Webbrowser.data[k].expiration_date < datetime.now().timestamp():
                    Webbrowser.data.pop(k)
            time.sleep(60)

    def get_page_content(self, message: MessageProtocol) -> bytes:
        render_data = Webbrowser.data.get(message.payload['id'])

        if render_data:
            return render_data.pickle_dump()

        return IRenderData(html=bytes(), expiration_date=0, javascript="", status_code=404).pickle_dump()

    def client_service(self, conn):
        try:
            while True:
                payload = conn.recv()
                message = MessageProtocol(**payload)

                if message.action == "render":
                    task_id = uuid.uuid4().hex
                    message.payload['id'] = task_id
                    self.queue.put(message)
                    conn.send(task_id)

                if message.action == "result":
                    conn.send(self.get_page_content(message))

                if message.action == "active_content":
                    data = self.get_content_active_page(message)
                    conn.send(data)

                # conn.send( payload )
        except EOFError:
            logger.info("Connect closed")

    def server(self, address, authkey):
        serv = Listener(address, authkey=authkey)

        with ThreadPoolExecutor(max_workers=4) as executor:

            for _ in count():
                try:
                    client = serv.accept()
                    executor.submit(self.client_service, client)
                except Exception:
                    traceback.print_exc()

    def run(self):
        try:
            logger.info(f"Selenium address: {self.config.SELENIUM_SERVER}")
            Thread(target=self.work_service, daemon=True).start()
            Thread(target=self.clear_service, daemon=True).start()
            self.server(
                self.config.SELENIUM_SERVER, authkey=self.config.KEY_SELENIUM_SERVER)
        finally:
            self.driver.quit()
            logger.info("Drop process")


class ElementsPresenceInDOM:
    """Check elements in DOM"""

    def __init__(self, css_selectors: List[str]):
        self.css_selectors = css_selectors

    def check_elements(self, driver: WebDriver):
        for css_selector in self.css_selectors:
            try:
                driver.find_element(By.CSS_SELECTOR, css_selector)
            except NoSuchElementException:
                return False
        return True

    def __call__(self, driver: WebDriver):

        return self.check_elements(driver)


wait_handler = {
    "ElementsPresenceInDOM" : ElementsPresenceInDOM
}