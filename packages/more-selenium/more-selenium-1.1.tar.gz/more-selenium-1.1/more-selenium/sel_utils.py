import random

from selenium import webdriver
# Stuff for waiting
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from . import audio_recognition, check_version


class Browser(check_version.ChromeDriver):
    def __init__(self, headless=False, proxy=None):
        """
        It creates a browser session and returns it
        
        :param headless: If True, the browser will run in headless mode, defaults to False (optional)
        :param proxy: The proxy server to use
        :param accs_list: The path to the file that contains the accounts to scrape, defaults to ./accs.txt
        (optional)
        """
        super(Browser, self).__init__()
        self.get_session(headless=headless, proxy=proxy)

    def solve_recaptcha(self, captcha_iframe):
        """
        The function takes in a captcha iframe and uses the audio recognition library to solve the captcha
        
        :param captcha_iframe: The iframe element that the captcha is located in
        """
        audio_recognition.reCAPTCHA(self, captcha_iframe)

    @staticmethod
    def random_username(n=12):
        """
        Generate a random string of length n from the chars a-z0-9
        
        :param n: The number of characters in the username, defaults to 12 (optional), defaults to 12
        (optional)
        :return: A string of random characters.
        """
        al = "abcdefghijklmnopqrstuvwxyz0123456789"
        return "".join([al[random.randint(0,len(al)-1)] for i in range(n)])

    def switch_to_iframe(self, xpath, timeout=10, by=By.XPATH):
        """
        Switch to embedded or single iframe specified by the xpath(s)
        
        :param xpath: The xpath of the iframe
        :param timeout: The amount of time in seconds to wait for the element to be present, defaults to 10
        (optional)
        :param by: By.XPATH, By.ID, By.NAME, etc
        """
        self.switch_to.default_content()
        if type(xpath) == str:
            self._switch_to_iframe(xpath, timeout, by)
        else:
            for path in xpath:
                self._switch_to_iframe(path, timeout, by)

    def _switch_to_iframe(self, xpath, timeout=10, by=By.XPATH):
        """
        Switch to an iframe using the xpath of the iframe
        
        :param xpath: The xpath of the iframe
        :param timeout: The maximum number of seconds to wait for the element to be present, defaults to 10
        (optional)
        :param by: By.XPATH, By.ID, By.CLASS_NAME, By.CSS_SELECTOR, By.NAME, By.LINK_TEXT,
        By.PARTIAL_LINK_TEXT, By.TAG_NAME, By.XPATH
        """
        self.switch_to.frame(self.get_and_wait(xpath=xpath, timeout=timeout, by=by))

    def get_and_wait(self, xpath, timeout=10, by=By.XPATH):
        """
        Wait for the element to be present in the DOM and then retrieve it
        
        :param xpath: The xpath of the element you want to find
        :param timeout: The amount of time we want to wait for the element to be present, defaults to 10
        (optional)
        :param by: The locator strategy to use
        :return: Nothing.
        """
        WebDriverWait(self, timeout).until(EC.presence_of_element_located((by, xpath)))
        return self.find_element_by_xpath(xpath)
