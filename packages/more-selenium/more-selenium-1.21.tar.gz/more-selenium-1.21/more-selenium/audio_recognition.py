import os
directory = '\\'.join(__file__.split('\\')[:-1])
os.environ["PATH"] = os.environ["PATH"] + f";{directory}\\audio_processing"

import pydub
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from speech_recognition import AudioFile, Recognizer


class reCAPTCHA:
    recognizer = Recognizer()
    def __init__(self, browser, iframe_location):
        self.browser = browser
        self.iframe_location = iframe_location
        self.switch_to_iframe(self.iframe_location)

        click_spot_1 = "/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]"
        self.get_and_wait(click_spot_1).click()

        # challenge_box_frame1 = "/html/body/div[1]/div/div[2]/div[3]/div/div/iframe"  # captcha box
        self.browser.switch_to.default_content()

        self.switch_to_iframe(self.iframe_location)

        challenge_box_frame2 = "/html/body/div[2]/div[2]/iframe"        # challenge box
        self.switch_to_iframe(challenge_box_frame2)

        click_spot_2 = "/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[2]/button"
        self.get_and_wait(click_spot_2).click()
        
        download_location = "/html/body/div/div/div[7]/a"
        url = self.get_and_wait(download_location).get_attribute("href")  # if this threw selenium.common.exceptions.TimeoutException then temporarily blocked.

        answer = self.mp3_url_to_text(url)
        text_box = "/html/body/div/div/div[6]/input"
        self.get_and_wait(text_box).send_keys(answer + Keys.ENTER)

        self.browser.switch_to.default_content()
        return answer

    def mp3_url_to_text(self, url):
        """
        It takes in an mp3 url and converts it to text.
        
        :param url: The URL of the MP3 file to be recognized
        :return: a string of the text that is transcribed from the audio file.
        """
        print(url)
        r = requests.get(url)
        with open("./audio.mp3", "wb") as f:
            f.write(r.content)
        pydub.AudioSegment.from_mp3(".\\audio.mp3").export(".\\audio.wav", format="wav")
        audio = AudioFile(".\\audio.wav")
        return self.recognize_text(audio)

    def recognize_text(self, file):
        """
        The function takes in a file and returns the text that was transcribed from that file
        
        :param file: The file object that you want to recognize
        :return: A string of the recognized audio.
        """
        with file as f:
            audio = self.recognizer.record(f)
        return self.recognizer.recognize_google(audio, language="en-US")

    def switch_to_iframe(self, xpath, timeout=10, by=By.XPATH):
        self.browser.switch_to.frame(self.get_and_wait(xpath=xpath, timeout=timeout, by=by))

    def get_and_wait(self, xpath, timeout=10, by=By.XPATH):
        """
        Wait for the element to be present in the DOM and then retrieve it
        
        :param xpath: The xpath of the element you want to find
        :param timeout: The amount of time we want to wait for the element to be present, defaults to 10
        (optional)
        :param by: The locator strategy to use
        :return: Nothing.
        """
        WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((by, xpath)))
        return self.browser.find_element_by_xpath(xpath)
