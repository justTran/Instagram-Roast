import autoit, os, time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pprint import pprint

class AutheticationError(Exception):
    pass

class Session():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.chrome_options = Options()
        self.chrome_options.add_argument('--window-size=1,1')
        self.chrome_options.add_argument('--autoplay-policy=false')
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--incognito')
        self.chrome_options.add_experimental_option("mobileEmulation", { "deviceName": "Nexus 5" })
        self.driver = webdriver.Chrome(options = self.chrome_options, executable_path = os.getcwd() + '/chromedriver.exe')
        self.wait = WebDriverWait(self.driver, 60)
        self.ui_elements = {
                            "loginButton" : "//*[@id='react-root']/section/main/article/div/div/div/div[2]/button",
                            "userField" : "//*[@id='react-root']/section/main/article/div/div/div/form/div[4]/div/label/input",
                            "passField" : "//*[@id='react-root']/section/main/article/div/div/div/form/div[5]/div/label/input",
                            "authenticate" : "//*[@id='react-root']/section/main/article/div/div/div/form/div[7]/button",
                            "invalidLogin" : "/html/body/div[4]/div/div/div[2]/button",
                            "saveInfoButton" : "//*[@id='react-root']/section/main/div/div/section/div/button",
                            "notNowButton" : "//*[@id='react-root']/section/main/div/div/div/button",
                            "uploadButton" : "//*[@id='react-root']/section/nav[2]/div/div/div[2]/div/div/div[3]",
                            "nextButton" : "//*[@id='react-root']/section/div[1]/header/div/div[2]/button",
                            "descriptionField" : "//*[@id='react-root']/section/div[2]/section[1]/div[1]/textarea",
                            "postButton" : "//*[@id='react-root']/section/div[1]/header/div/div[2]/button",                          
                            }

    def authenticate(self):
        try:
            self.driver.get("https://instagram.com")
            time.sleep(10)
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["loginButton"]))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["userField"]))).send_keys(self.username)
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["passField"]))).send_keys(self.password)
            time.sleep(1)
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["authenticate"]))).click()
            try:
                time.sleep(6)
                try: 
                    if self.driver.find_element_by_xpath(self.ui_elements["invalidLogin"]):
                        raise AutheticationError

                except NoSuchElementException as e: 
                    self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["notNowButton"]))).click()
                    return True

            except NoSuchElementException as e:
                time.sleep(12)
                try: 
                    if self.driver.find_element_by_xpath(self.ui_elements["invalidLogin"]):
                        raise AutheticationError

                except NoSuchElementException as e: 
                    self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["notNowButton"]))).click()
                    return True

        except AutheticationError as e:
            return False

    def uploadImage(self, image_path, description):
        upload = self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["uploadButton"])))
        webdriver.ActionChains(self.driver).move_to_element(upload).click().perform()
        autoit.win_wait("[CLASS:#32770; TITLE:Open]", 60)
        autoit.control_set_text("[CLASS:#32770; TITLE:Open]", "Edit1", image_path)
        autoit.control_click("[CLASS:#32770; TITLE:Open]", "Button1")
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["nextButton"]))).click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["descriptionField"]))).send_keys(description)
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.ui_elements["postButton"]))).click()

    def destroy(self):
        try:
            self.driver.close()
        except:
            pass