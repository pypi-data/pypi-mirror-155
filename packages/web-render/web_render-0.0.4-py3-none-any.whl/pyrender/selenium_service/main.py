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
from webdriver_manager.chrome import ChromeDriverManager
from multiprocessing.connection import Listener
from queue import Queue
from itertools import count
from threading import Thread
from pyrender.tool import log
from pyrender.interface import MessageProtocol, IRenderData
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import Dict
from selenium_stealth import stealth


logger = log(__name__)


class Webbrowser:

    data: Dict[str, IRenderData] = dict()
    queue = Queue()

    def __init__(self, config):
        self.config = config
        co = Options()
        if self.config.PROXY_SERVER:
            co.add_argument(
                "--proxy-server={}".format(self.config.PROXY_SERVER))
        if self.config.HEADLESS:
            co.add_argument('--headless')

        co.add_argument('--disable-blink-features=AutomationControlled')
        co.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        co.add_experimental_option("excludeSwitches", ["enable-automation"])
        if self.config.DISABLE_IMAGE:
            chrome_prefs = {}
            chrome_prefs["profile.default_content_settings"] = {"images": 2}
            chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
            co.add_experimental_option("prefs", chrome_prefs)
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=co)

        # self.driver.set_page_load_timeout(self.config.LOAD_TIMEOUT)
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

    def set_url(self, message: MessageProtocol):
        self.driver.get(message.payload['url'])
        js_data = None

        if message.payload['wait']:
            time.sleep(float(message.payload['wait']))

        if message.payload['jscript']:
            result = self.driver.execute_script(message.payload['jscript'])
            if isinstance(result, int) or isinstance(result, str):
                js_data = result
            time.sleep(0.15)

        Webbrowser.data[message.payload['id']] = IRenderData(
            html=IRenderData.compress_zlib(self.driver.page_source),
            expiration_date=message.payload['expiration_date'],
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

        return IRenderData(html=bytes(), expiration_date=0, javascript="").pickle_dump()

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
            logger.info("Connected close")

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
