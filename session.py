import autoit
import os
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class AutheticationError(Exception):
    pass

class Session():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--autoplay-policy=false')
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--incognito')
        self.driver = webdriver.Chrome(options = self.chrome_options, executable_path = os.getcwd() + '\\msedgedriver.exe')
        self.wait = WebDriverWait(self.driver, 20)
        self.ui_elements = {
                            "loginButton" : "//*[@id='loginForm']/div/div[3]/button",
                            "userField" : "//*[@id='loginForm']/div/div[1]/div/label/input",
                            "passField" : "//*[@id='loginForm']/div/div[2]/div/label/input",
                            "invalidLogin" : "//*[@id='slfErrorAlert']",
                            "notNowButton" : "//*[@id='react-root']/section/main/div/div/div/div/button",
                            "notNowButton2" : "/html/body/div[5]/div/div/div/div[3]/button[2]",
                            "uploadButton" :"//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[3]/div/button",
                            "selectFrom" : "/html/body/div[8]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div[2]/div/button",
                            "nextButton" : "/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button",
                            "descriptionField" : "/html/body/div[6]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea",
                            "postButton" : "/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button",                     
                            }

    def authenticate(self):
        try:
            self.driver.get("https://instagram.com")
            time.sleep(10)
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["userField"]))).send_keys(self.username)
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["passField"]))).send_keys(self.password)
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["loginButton"]))).click()
            try:
                time.sleep(2)
                try: 
                    if self.driver.find_element_by_xpath(self.ui_elements["invalidLogin"]):
                        raise AutheticationError

                except NoSuchElementException as e: 
                    try:
                        self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["notNowButton"]))).click()
                        self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["notNowButton2"]))).click()
                    except:
                        pass

                    return True

            except NoSuchElementException as e:
                time.sleep(4)
                try: 
                    if self.driver.find_element_by_xpath(self.ui_elements["invalidLogin"]):
                        raise AutheticationError

                except NoSuchElementException as e:
                    try:
                        self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["notNowButton"]))).click()
                        self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["notNowButton2"]))).click()
                    except:
                        pass

                    return True

        except AutheticationError as e:
            return False

    def uploadImage(self, image_path, description):
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["uploadButton"]))).click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["selectFrom"]))).click()
        self.eventHandler(image_path)
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["nextButton"]))).click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["nextButton"]))).click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["descriptionField"]))).send_keys(description)
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["postButton"]))).click()

    def eventHandler(self, image_path):
        autoit.win_wait("[CLASS:#32770; TITLE:Open]", 60)
        autoit.control_set_text("[CLASS:#32770; TITLE:Open]", "Edit1", image_path)
        autoit.control_click("[CLASS:#32770; TITLE:Open]", "Button1")       

    def destroy(self):
        try:
            self.driver.close()
        except:
            pass