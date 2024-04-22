from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def send(sendAnswear, prompt_area, driver, prompt):
    wait = WebDriverWait(driver, 10)
    waitLong = WebDriverWait(driver, 100)

    print('send prompt: '+str(prompt))
    prompt_area.click()
    time.sleep(0.5)
    prompt_area.send_keys(prompt)
    wait.until(EC.text_to_be_present_in_element((By.ID, 'prompt-textarea'), prompt))
    prompt_area.send_keys(Keys.ENTER)
    print('вопрос задан')

    wait.until(
        EC.presence_of_element_located((By.XPATH, f'//div[contains(text(), "{prompt}")]/ancestor::div[@data-testid]'))
    )
    testid = driver.find_element(By.XPATH, f'//div[contains(text(), "{prompt}")]/ancestor::div[@data-testid]')
    turn = testid.get_attribute("data-testid")
    if(turn == 'conversation-turn-1'):
        turn = 'conversation-turn-2'
    target_turn = str(int(turn.split('-')[2]) + 1)

    wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@data-testid="conversation-turn-{target_turn}"]')))
    print('ответ в процессе')

    waitLong.until(
        EC.text_to_be_present_in_element_attribute(
            (By.XPATH, f'//*[@data-testid="conversation-turn-{target_turn}"]/descendant::div[@data-message-author-role="assistant"]/div'),
            'class',
            'result-streaming'
        )
    )

    print('chatGPT пишет...')
    waitLong.until_not(
        EC.text_to_be_present_in_element_attribute(
            (By.XPATH, f'//*[@data-testid="conversation-turn-{target_turn}"]/descendant::div[@data-message-author-role="assistant"]/div'),
            'class',
            'result-streaming'
        )
    )
    print('ответ готов')

    answear = driver.find_element(By.XPATH, f'//*[@data-testid="conversation-turn-{target_turn}"]/descendant::div[@data-message-author-role="assistant"]/div')
    sendAnswear(answear.get_attribute("outerHTML"))
    










