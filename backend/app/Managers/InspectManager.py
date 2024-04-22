import time

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


class InspectManager:
    SEARCH_TYPES = {
        "name": By.NAME,
        "class": By.CLASS_NAME,
        "x_path": By.XPATH
    }
    WAIT = 3

    def __init__(self, proxy=None, device=None, cookies=None, headless=True, url=None, actions=None):
        self.proxy = proxy
        self.device = device
        self.cookies = cookies
        self.headless = headless

        self.url = url
        self.actions = actions

        self.web_driver = None

    def set_driver(self):
        browser_options = Options()
        proxy_options = None

        if self.headless:
            browser_options.add_argument("--headless")

        if self.proxy and self.proxy.login and self.proxy.password and self.proxy.ip and self.proxy.port and self.proxy.ssl:
            proxy_options = {
                "proxy": {
                    "http": f"http://{self.proxy.login}:{self.proxy.password}@{self.proxy.ip}:{self.proxy.port}",
                    "verify_ssl": self.proxy.ssl
                }
            }

        # # disable sandbox mode
        # browser_options.add_argument('--no-sandbox')

        # SET WEB DRIVER
        self.web_driver = webdriver.Chrome(
            options=browser_options,
            seleniumwire_options=proxy_options if proxy_options is not None else None
        )

        # SET WINDOW SIZE
        if self.device and self.device.user_agent:
            self.web_driver.set_window_size(
                self.device.user_agent["screenWidth"],
                self.device.user_agent["screenHeight"],
            )

        # SET COOKIES
        if self.cookies:
            self.web_driver.execute_cdp_cmd('Network.enable', {})
            for cookie in self.cookies:
                # Fix issue Chrome exports 'expiry' key but expects 'expire' on import
                if 'expiry' in cookie:
                    cookie['expires'] = cookie['expiry']
                    del cookie['expiry']
                self.web_driver.execute_cdp_cmd('Network.setCookie', cookie)
            self.web_driver.execute_cdp_cmd('Network.disable', {})

    def get_form_elements(self, form=None, elements=None):
        result = []

        try:
            parent_form = WebDriverWait(self.web_driver, self.WAIT).until(
                EC.presence_of_element_located((
                    form.form_attribute,
                    form.form_attribute_name
                ))
            )

            for element in elements:
                child_el = parent_form.find_element(
                    by=self.SEARCH_TYPES[element.component_attribute],
                    value=element.component_attribute_name
                )

                if not child_el.is_displayed():
                    raise Exception("form component is not displayed")
                if not child_el.is_enabled():
                    raise Exception("form component is not enabled")

                element.selenium_obj = child_el
                result.append(element)

        except NoSuchElementException as e:
            print("Can't find element")
            result = []
        except TimeoutException as e:
            print("Timeout. Can't find element")
            result = []
        except Exception as e:
            print(e)
            result = []

        return result

    def run_pre_check_actions(self, elements=None):
        try:

            for el in elements:
                el.selenium_obj = self.web_driver.find_element(By.XPATH, el.x_path)
                el.selenium_obj.click()
                time.sleep(5)

        except NoSuchElementException as e:
            print("Can't find element")
        except TimeoutException as e:
            print("Timeout. Can't find element")
        except Exception as e:
            print(e)

    def start(self):
        self.set_driver()
        self.web_driver.get(self.url)
        try:
            for action in self.actions:
                el = self.web_driver.find_element(
                    self.SEARCH_TYPES[action.search_type],
                    action.search_value
                )

                if not el.is_enabled():
                    raise Exception(f"{vars(action)} is not enabled")
                if not el.is_displayed():
                    raise Exception(f"{vars(action)} is not displayed")

                if action.action == "click":
                    el.click()
                elif action.action == "send_keys":
                    el.send_keys(action.action_value)
                elif action.action == "select":
                    select = Select(el)
                    select.select_by_visible_text(action.action_value)

                time.sleep(1)

        except NoSuchElementException as e:
            print("Can't find element")
        except TimeoutException as e:
            print("Timeout. Can't find element")
        except Exception as e:
            print(e)

        time.sleep(10)