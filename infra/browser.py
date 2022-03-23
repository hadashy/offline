import logging
from typing import Optional
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import InvalidArgumentException, NoSuchElementException
from urllib3.exceptions import MaxRetryError


logger = logging.getLogger(__name__)


BROWSER_DEFAULT = DesiredCapabilities.CHROME


def _connect_selenium() -> WebDriver:
    try:
        driver = webdriver.Remote(
            desired_capabilities=BROWSER_DEFAULT)
    except MaxRetryError as error:
        raise Exception("Connect web driver failed check if webdriver open") from error
    logger.info("selenium web driver created successfully")
    return driver


class BrowserManager:
    def __init__(self, _driver: webdriver):
        self._driver: WebDriver = _driver

    @property
    def driver(self) -> WebDriver:
        if not self._driver:
            self._driver = _connect_selenium()
        return self._driver

    def close_browser(self) -> None:
        logger.info("browser closed")
        self.driver.close()
        self._driver = None

    def launch_url(self, url: str) -> None:
        logger.info(f"browser try launch - {url}")
        try:
            self.driver.get(url)
        except InvalidArgumentException as error:
            if not url.startswith(r"https:\\"):
                logger.info(r"get request failed try to add https:\\ to requests")
                self.launch_url(r"https:\\" + url)
            else:
                raise Exception(f"{url} is invalid") from error

    def find_element_by_id(self, element_id: str) -> Optional[WebElement]:
        try:
            logger.debug(f"looking for {element_id}")
            return self.driver.find_element_by_id(element_id)
        except NoSuchElementException:
            logger.info(f"element id - {element_id} not found in page")
            return None

    def find_element_by_name(self, element_id: str) -> Optional[WebElement]:
        try:
            logger.debug(f"looking for {element_id}")
            return self.driver.find_element_by_name(element_id)
        except NoSuchElementException:
            logger.info(f"element id - {element_id} not found in page")
            return None

    def find_element_by_xpath(self, element_xpath: str) -> Optional[WebElement]:
        try:
            logger.debug(f"looking for {element_xpath}")
            return self.driver.find_element_by_xpath(element_xpath)
        except NoSuchElementException:
            logger.info(f"element id - {element_xpath} not found in page")
            return None

    def click_on_element_by_name(self, element_id: str) -> None:
        button = self.find_element_by_name(element_id)
        if not button:
            raise Exception(f"element {element_id} not found")
        button.click()

    def click_on_element_by_id(self, element_id: str) -> None:
        button = self.find_element_by_id(element_id)
        if not button:
            raise Exception(f"element {element_id} not found")
        button.click()

    def send_text_to_field(self, field_id: str, text: str) -> None:
        field = self.find_element_by_id(field_id)
        if not field:
            raise Exception(f"element {field} not found")
        self.send_keys_to_element(field, text)

    def get_element_text_by_id(self, element_id: str) -> str:
        element = self.find_element_by_id(element_id)
        if not element:
            raise Exception(f"element {element_id} id not found")
        return self.get_element_text(element)

    @staticmethod
    def get_element_text(element: WebElement) -> str:
        return element.text

    @staticmethod
    def send_keys_to_element(element: WebElement, text: str) -> None:
        element.send_keys(text)
