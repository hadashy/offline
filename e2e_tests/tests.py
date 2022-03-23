import pytest
from selenium import webdriver
from infra.tests_actions.chrome import validate_main_tab
from infra.browser import BrowserManager
from infra.tests_actions.calc import validate_result, close_program, err


@pytest.mark.full_checks
@pytest.mark.calc
def test_validate_calculator() -> None:
    validate_result()
    close_program()


@pytest.mark.full_checks
@pytest.mark.calc
def test_validate_err() -> None:
    err()


@pytest.mark.full_checks
@pytest.mark.chrome
def test_validate_ynet_main_tab(
        driver: BrowserManager = BrowserManager(webdriver.Chrome()),
        wait_timeout: int = 5
) -> None:
    validate_main_tab(driver, wait_timeout)
    driver.close_browser()

#  pytest tests.py -m full_checks -vv --no-header -rfp > reports/report.txt
#  (then we can call reports.py -> parse_reports_file)
