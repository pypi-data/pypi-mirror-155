import re
import time
import zipfile
from sys import platform

import requests
from selenium import webdriver
from selenium.common import exceptions as expt


class ChromeDriver(webdriver.Chrome):
    def __init__(self, verbose=True):
        self.v = verbose
        self.update_url = "https://chromedriver.chromium.org/downloads"
        self.version_url = "https://chromedriver.storage.googleapis.com/index.html?path="
        self.version_regex = r"([0-9]{1,4}\.){3}[0-9]{1,4}"

        if platform == "linux" or platform == "linux2":
            self.zip_fn = "chromedriver_linux64.zip"
        elif platform == "darwin":
            self.zip_fn = "chromedriver_mac64.zip"
        elif platform == "win32":
            self.zip_fn = "chromedriver_win32.zip"

        self.bin_path = "https://chromedriver.storage.googleapis.com/{0}/" + self.zip_fn

    def update(self, version=None):
        """
        It downloads the latest version of chromedriver and extracts it.
        
        :param version: The version of chromedriver you want to download. If None, it will download the
        latest version
        """
        if self.v:
            print("Automatically updating now...")
        version = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE").text
        if version is None:
            r = requests.get(self.update_url)
            t = r.text
            g = re.search(self.version_regex, t).group()
            v_url = self.bin_path.format(g)
        else:
            v_url = self.bin_path.format(version)

        if self.v:
            print(f"Downloading {v_url}")
        chromedriver = requests.get(v_url)

        out_dir = "./"
        zip_dir = f"{out_dir}{self.zip_fn}"
        with open(zip_dir, "wb") as f:
            f.write(chromedriver.content)

        print(f"Extracting {zip_dir}")
        try:
            with zipfile.ZipFile(zip_dir, "r") as zip_ref:
                zip_ref.extractall(out_dir)
        except zipfile.BadZipFile as e:
            raise zipfile.BadZipFile(str(e) + f". The version {version} is not a valid chromedriver version.")

        print("Done.")

    def get_session(self, headless=True, auto_update=True, proxy=None):
        """
        If the chromedriver is not in the directory, download it. If the chromedriver is not the right
        version, update it
        
        :param headless: If True, the browser will run in headless mode, i.e., without a UI or display
        server dependencies, defaults to True (optional)
        :return: A session object that can be used to navigate the browser.
        """
        try:
            return self._get_session(headless, proxy)
        except expt.SessionNotCreatedException as e:
            print(e)
            error_message = str(e)
            version = re.search(self.version_regex, error_message).group()
            if self.v:
                print(f"Update chromedriver required! {self.update_url}")
            if auto_update:
                self.update(version=version)
                return self._get_session(headless, proxy)
        except expt.WebDriverException:
            if self.v:
                print(f"Chromedriver not in directory! {self.update_url}")
            if auto_update:
                self.update()                   # Get a version of chromeriver
                return self.get_session(headless)      # Get the right version of chromedriver

    def _get_session(self, headless, proxy):
        """
        This function creates a new browser session and returns it.
        
        :param headless: If True, the browser's GUI won't be shown
        :return: A browser session that can be used to query the website.
        """
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('headless')
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")
        # options.add_argument('--ignore-certificate-errors')
        super(ChromeDriver, self).__init__("./chromedriver.exe", options=options)

if __name__ == "__main__":
    a = ChromeDriver()
    sess = a.get_session()
