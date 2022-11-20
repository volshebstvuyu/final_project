from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import consts
import time

def get_driver():
    try:
        driver = webdriver.Firefox(executable_path = consts.driverPathMozilla)
    except:
        driver = webdriver.Chrome(executable_path = consts.driverPathChrome)

    driver.get(consts.baseUrl)
    driver.maximize_window()    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'forgot_password'))).click()
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Восстановление пароля'
    return driver, wait

def check_captcha_refresh(driver: webdriver, wait: WebDriverWait, oldCaptcha: str):
    driver.find_element(By.ID, ('reset')).click()
    newCaptcha = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rt-captcha__image'))).get_attribute('src')

    title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.card-container__error')))
    assert title.text == 'Неверный логин или текст с картинки'

    assert oldCaptcha != newCaptcha

    time.sleep(3)
    driver.quit()


def test_form_change():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    tabButtons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'rt-tab')))
    assert wait.until(EC.title_is('Ростелеком ID'))
    assert len(tabButtons) == 4

    for i in range(len(tabButtons)):
        actionChain.move_to_element(tabButtons[i]).click().perform()
        placeholderInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-input__placeholder'))).text
        assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, consts.activeTab))).text == driver.find_element(By.ID, consts.tabButtonsId[i]).text
        assert placeholderInput == consts.placeholderInputsValue[i]


def test_restore_with_mobile_phone():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    placeholderInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-input__placeholder'))).text
    assert placeholderInput == consts.placeholderInputsValue[0]
    oldCaptcha = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rt-captcha__image'))).get_attribute('src')

    actionChain.move_to_element(driver.find_element(By.ID, 'username')).click().perform()
    actionChain.send_keys(consts.sendedKeys[0]).perform()

    actionChain.move_to_element(driver.find_element(By.ID, 'captcha')).click().perform()
    actionChain.send_keys(consts.sendedKeyCaptcha).perform()
    
    activeTabButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'.rt-tabs .{consts.activeTab}')))
    assert activeTabButton.text == consts.tabTitles[0]

    check_captcha_refresh(driver, wait, oldCaptcha)


def test_restore_with_email():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    placeholderInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-input__placeholder'))).text
    assert placeholderInput == consts.placeholderInputsValue[0]
    oldCaptcha = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rt-captcha__image'))).get_attribute('src')

    actionChain.move_to_element(driver.find_element(By.ID, 'username')).click().perform()
    actionChain.send_keys(consts.sendedKeys[1]).perform()

    actionChain.move_to_element(driver.find_element(By.ID, 'captcha')).click().perform()
    actionChain.send_keys(consts.sendedKeyCaptcha).perform()
    
    activeTabButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'.rt-tabs .{consts.activeTab}')))
    assert activeTabButton.text == consts.tabTitles[1]

    check_captcha_refresh(driver, wait, oldCaptcha)


def test_restore_with_login():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    placeholderInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-input__placeholder'))).text
    assert placeholderInput == consts.placeholderInputsValue[0]
    oldCaptcha = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rt-captcha__image'))).get_attribute('src')

    actionChain.move_to_element(driver.find_element(By.ID, 'username')).click().perform()
    actionChain.send_keys(consts.sendedKeys[2]).perform()

    actionChain.move_to_element(driver.find_element(By.ID, 'captcha')).click().perform()
    actionChain.send_keys(consts.sendedKeyCaptcha).perform()
    
    activeTabButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'.rt-tabs .{consts.activeTab}')))
    assert activeTabButton.text == consts.tabTitles[2]

    check_captcha_refresh(driver, wait, oldCaptcha)


def test_restore_with_ls():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    placeholderInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-input__placeholder'))).text
    assert placeholderInput == consts.placeholderInputsValue[0]
    oldCaptcha = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rt-captcha__image'))).get_attribute('src')

    actionChain.move_to_element(driver.find_element(By.ID, 'username')).click().perform()
    actionChain.send_keys(consts.sendedKeys[3]).perform()

    actionChain.move_to_element(driver.find_element(By.ID, 'captcha')).click().perform()
    actionChain.send_keys(consts.sendedKeyCaptcha).perform()
    
    activeTabButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'.rt-tabs .{consts.activeTab}')))
    assert activeTabButton.text == consts.tabTitles[3], driver.quit()
    check_captcha_refresh(driver, wait, oldCaptcha)


def test_refresh_captca():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    oldCaptcha = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rt-captcha__image'))).get_attribute('src')
    actionChain.move_to_element(driver.find_element(By.CLASS_NAME, 'rt-captcha__reload')).click().perform()

    driver.implicitly_wait(20)

    newCaptcha = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rt-captcha__image'))).get_attribute('src')
    assert oldCaptcha != newCaptcha


def test_correct_return_to_auth_page():
    driver, wait = get_driver()

    wait.until(EC.presence_of_element_located((By.ID, 'reset-back'))).click()
    assert wait.until(EC.presence_of_element_located((By.XPATH, '//h1[@class="card-container__title"]'))).text == 'Авторизация'

    driver.quit()
