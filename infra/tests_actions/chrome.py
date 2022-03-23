import logging
import time
import selenium.common.exceptions
from selenium.webdriver import Keys
from infra.browser import BrowserManager
from infra.utils import retry


chrome_data = dict(
    site_path='http://www.google.com',
    search_txt='ynet',
    site_txt='/html/body/div[7]/div/div[10]/div[1]/div[2]/div[2]/'
             'div/div/div[1]/div/div/div/div/div/div/div[1]/a/h3',
)

chrome_xpath = dict(
    search='/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input',
    main_tab='/html/body/div[7]/div/div/div[1]/div[3]/div/div/'
             'span/span/div/div[2]/div[1]/div[1]/div[1]/a/span',
)


logger = logging.getLogger(__name__)


def commit_search(driver: BrowserManager) -> None:
    search_input = driver.find_element_by_xpath(chrome_xpath['search'])
    if not search_input:
        raise Exception(f"Element {chrome_xpath['search']} wasn't found")
    driver.send_keys_to_element(search_input, chrome_data['search_txt'] + Keys.ENTER)
    site_txt = driver.find_element_by_xpath(chrome_data['site_txt'])
    if not site_txt:
        raise Exception(f"Site {chrome_data['site_txt']} wasn't found")
    logger.info(f"Commited search {chrome_xpath['search']}")
    site_txt.click()


@retry(3, 3)
def validate_main_tab(driver: BrowserManager, wait_timeout: int = 5) -> None:
    try:
        driver.launch_url(chrome_data['site_path'])
    except selenium.common.exceptions.WebDriverException as err:
        logger.error(f"Site wasn't opened - error {err}")
    commit_search(driver)
    time.sleep(wait_timeout)
    logger.info(f"Searching for {chrome_xpath['main_tab']}")
    article = driver.find_element_by_xpath(chrome_xpath['main_tab'])
    assert article, f"Tab {chrome_xpath['main_tab']} wasn't found"
