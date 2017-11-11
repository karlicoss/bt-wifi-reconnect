#!/usr/bin/env python3.6

from selenium import webdriver # type: ignore
from selenium.webdriver.remote.webdriver import WebDriver # type: ignore
from selenium.webdriver import Chrome, Firefox, PhantomJS # type: ignore
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities # type: ignore

from subprocess import check_call

import config

from kython import *

_LOGGER_TAG = 'BTReloginHelper'


class ReloginHelper:
    def __init__(self, username: str, password: str) -> None:
        self.logger = logging.getLogger(_LOGGER_TAG)
        self.config = config
        self.username = username
        self.password = password

    def _login(self, driver: WebDriver):
        driver.get("https://www.btopenzone.com:8443/home")  # trigger login
        # TODO huh, on VPN it shows 'you may have lost connection'. weird.

        # select 'BT Wi-fi
        driver.find_element_by_id("provider2").click()

        # for some reason every bt wifi option (FON/Broadband/Wifi) has its own form
        # so we have to find the one responsible for BT WiFI login
        login_form = driver.find_element_by_id('wifi_logon_form')

        login_form.find_element_by_id("username").send_keys(self.username)
        login_form.find_element_by_id("password").send_keys(self.password)
        login_form.find_element_by_id("loginbtn").click()

    def _check_connected(self) -> bool:
        # testing for internet connection is hard..
        # ideally you should just ping, but on BT DNS works once you are connected, you don't have to log in
        # so we load a small http page and check its content to see if we have access to Internet
        try:
            import urllib.request
            TIMEOUT_SECONDS = 3
            url = urllib.request.urlopen("https://httpbin.org/get?hasinternet=True", None, TIMEOUT_SECONDS)
            data = str(url.read(), 'utf-8')
            return "hasinternet" in data
        except Exception:  # too broad exception type.. but whatever, what could go wrong here
            self.logger.exception("Exception while trying to load test page")
            return False

    def login_if_necessary(self):
        # TODO sanity check that we are connected to BT wifi?
        if self._check_connected():
            self.logger.debug("Connected.. no action needed")
            return

        self.logger.info("Not connected.. launching webdriver to log in")

        driver = webdriver.PhantomJS(
            executable_path=self.config.PHANTOMJS_BIN,
            # sometimes returns empty page...
            # see https://stackoverflow.com/a/36159299/706389
            service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1']
        )
        try:
            driver.maximize_window()
            self._login(driver)
            self.logger.info("Logged in via PhantomJS")
        finally:
            driver.quit()

    def reconnect_wifi(self):
        btwifi = "BTWifi-with-FON"
        name = get_wifi_name()
        if name != btwifi:
            self.logger.warning(f"Current network is {name}, will not attempt reconnecting!")
            return

        self.logger.info(f"Disabling connection...")
        check_call(["nmcli", "con", "down", btwifi])
        self.logger.info(f"sleeping...")
        import time
        time.sleep(5)
        self.logger.info(f"Enabling connection...")
        check_call(["nmcli", "con", "up", btwifi])

    def fix_wifi(self):
        self.login_if_necessary()
        # TODO determine when is it necessary to reconnect


def main():
    setup_logging()

    helper = ReloginHelper(config.USERNAME, config.PASSWORD)
    helper.login_if_necessary()


if __name__ == '__main__':
    main()
