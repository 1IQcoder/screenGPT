# Разкомментировать перед сборкой:
import sys, io
buffer = io.StringIO()
sys.stdout = sys.stderr = buffer
# -------------------------------
import eel
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc
from functions import logIn, waitFor, JsonFile
from prompt import send
import keyboard as kb
import time
import json
import os


def AppData_folder():
    appdata_path = os.getenv('APPDATA')
    folder_path = os.path.join(appdata_path, 'screenGPT')

    try:
        os.makedirs(folder_path)
        print("Папка успешно создана")
    except FileExistsError:
        print("Папка уже существует")
    except Exception as e:
        print("Возникла ошибка при создании папки:", e)

    data = {
        "email": "",
        "password": "",
        "auto_login": ""
    }

    json_file_path = os.path.join(folder_path, "data.json")
    if not os.path.exists(json_file_path):
        print("Файл data.json не найден в папке", folder_path)
        try:
            with open(json_file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print("Файл data.json успешно создан.")
        except Exception as e:
            print("Возникла ошибка при создании файла data.json:", e)
AppData_folder()


driver = None
window = False
wait = None


@eel.expose
def createDriver():
    global wait
    global driver
    driver = uc.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    return True


@eel.expose
def start():
    driver.get('https://chat.openai.com/')
    driver.maximize_window()

    json_file_data = JsonFile.read()
    email = json_file_data['email']
    password = json_file_data['password']
    auto_login = json_file_data['auto_login']

    if auto_login == 'true' and len(email)>0 and len(password)>0:
        waitFor(driver, 'TAG_NAME', 'body')
        logIn(driver, wait, email, password)
    else:
        print("Анонимный сеанс")

    time.sleep(3)


@eel.expose
def quit():
    if not driver == None:
        driver.quit()
    return False


@eel.expose
def sendPrompt(prompt):
    data = json.loads(prompt)
    content = data['data']
    prompt_area = driver.find_element(By.ID, 'prompt-textarea')
    send(sendAnswear, prompt_area, driver, str(content))
    eel.alertMessage('Ожидание ответа', 'green')
    

def close_window(e):
    if e.event_type != kb.KEY_UP:
        return
    global window
    if window:
        eel.close_window()
        window = False
    elif not window:
        eel.open_window()
        window = True


def sendAnswear(htmlText):
    eel.insertAnswear(htmlText)


# json file
@eel.expose
def writeJson(data):
    JsonFile.replace(data)

@eel.expose
def getJson():
    return JsonFile.read()

kb.hook_key('f7', close_window)

eel.init('web', allowed_extensions=['.html', '.css', '.txt', '.js'])
eel.start('index.html', size=(500, 400))











