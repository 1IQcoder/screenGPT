import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os

appdata_path = os.getenv('APPDATA')
new_folder_path = os.path.join(appdata_path, 'screenGPT')
json_file_path = os.path.join(new_folder_path, "data.json")

class JsonFile:
    def read():
        with open(json_file_path) as f:
            data = json.load(f)
            return data
        
    def write(data):
        json_object = json.dumps(data, indent=4)
        with open(json_file_path, "w") as f:
            f.write(json_object)

    def replace(dictionary):
        oldData = JsonFile.read()
        oldData.update(dictionary)
        JsonFile.write(oldData)


by_type_obj = {
    'CLASS_NAME': By.CLASS_NAME,
    'NAME': By.NAME,
    'TAG_NAME': By.TAG_NAME,
    'CSS_SELECTOR': By.CSS_SELECTOR,
    'ID': By.ID,
    'XPATH': By.XPATH
}
def waitFor(driver, BYtype, elemName):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((by_type_obj[BYtype], elemName)))


def logIn(driver, wait, email, password):
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button/div[contains(text(), "Log in")]')))
        driver.find_element(By.XPATH, '//button/div[contains(text(), "Log in")]').click()
        print('Вход в аккаунт...')

        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="email-input"]')))
        email_input = driver.find_element(By.XPATH, '//input[@id="email-input"]')
        email_input.click()
        time.sleep(0.5)
        email_input.send_keys(email)

        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="continue-btn"]')))
        driver.find_element(By.XPATH, '//button[@class="continue-btn"]').click()

        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="password"]')))
        passwrd_input = driver.find_element(By.XPATH, '//input[@id="password"]')
        passwrd_input.click()
        time.sleep(0.5)
        passwrd_input.send_keys(password)

        wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]')))
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    except:
        print("Анонимный сеанс")


def saveCookies(driver):
    cookies = driver.get_cookies()
    with open('cookies.txt', 'w') as file:
        json.dump(cookies, file)


def loadCookies(driver):
    try:
        with open('cookies.txt', 'r') as file:
            cookies = json.load(file)
            for cookie in cookies:
                print(cookie)
                driver.add_cookie(cookie)

    except Exception as e:
        print("Произошла ошибка с Cookies:", e)
    else:
        print('Ошибка Cookies')
    finally:
        return
    


