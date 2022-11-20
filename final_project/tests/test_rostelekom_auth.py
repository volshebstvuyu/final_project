from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import consts
import time
import locale

def get_driver():
    try:
        driver = webdriver.Firefox(executable_path = consts.driverPathMozilla)
    except:
        driver = webdriver.Chrome(executable_path = consts.driverPathChrome)

    driver.get(consts.baseUrl)
    driver.maximize_window()    
    wait = WebDriverWait(driver, 40)

    assert wait.until(EC.presence_of_element_located((By.XPATH, '//h1[@class="card-container__title"]'))).text == 'Авторизация'
    return driver, wait


def check_auth_failed(driver: webdriver, wait: WebDriverWait):
    driver.find_element(By.ID, ('kc-login')).click()
    
    driver.implicitly_wait(40)
    forgetLink = driver.find_element(By.LINK_TEXT, 'Забыл пароль')
    classesOfforgetLink = forgetLink.get_attribute('class')
    
    if check_captcha_visibility(driver, wait):
        title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.card-container__error')))
        assert title.text == 'Неверно введен текст с картинки'
    else:
        title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.card-container__error.login-form-container__error--bold')))
        assert title.text != 'Неверный логин или пароль'
        assert classesOfforgetLink.__contains__('rt-link--orange')
    
    time.sleep(3)
    driver.quit()


def check_captcha_visibility(driver: webdriver, wait: WebDriverWait):
    try:
        wait.until(EC.visibility_of_element_located((By.ID, 'captcha')))
        return True
    except:
        return False


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
        assert placeholderInput == consts.placeholderInputsValue[i], driver.quit()


def test_correct_change_input():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)
    
    tabButtons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'rt-tab')))

    placeholderInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-input__placeholder'))).text
    assert placeholderInput == consts.placeholderInputsValue[0]

    for i in range(len(tabButtons)):
        actionChain.move_to_element(driver.find_element(By.ID, 'username')).click().perform()
        actionChain.send_keys(consts.sendedKeys[i]).perform()

        actionChain.move_to_element(driver.find_element(By.ID, 'password')).click().perform()
        
        activeTabButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'.rt-tabs .{consts.activeTab}')))
        assert activeTabButton.text == consts.tabTitles[i], driver.quit()

        time.sleep(1) # Имитация живого пользователя

        actionChain.double_click(driver.find_element(By.ID, 'username')).click_and_hold().send_keys(Keys.DELETE).perform()
        time.sleep(1)
    
    driver.quit()



def test_correct_input_phone_number():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    placeholderInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-input__placeholder'))).text
    assert placeholderInput == consts.placeholderInputsValue[0]

    actionChain.move_to_element(driver.find_element(By.ID, 'username')).click().perform()
    actionChain.send_keys('9160123456').perform()

    actionChain.move_to_element(driver.find_element(By.ID, 'password')).click().perform()
    actionChain.send_keys('Qwertyui').perform()
    
    activeTabButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'.rt-tabs .{consts.activeTab}')))
    assert activeTabButton.text == consts.tabTitles[0]

    check_auth_failed(driver, wait)


def test_correct_input_email():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    placeholderInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-input__placeholder'))).text
    assert placeholderInput == consts.placeholderInputsValue[0]

    actionChain.move_to_element(driver.find_element(By.ID, 'username')).click().perform()
    actionChain.send_keys('test@test.ru').perform()

    actionChain.move_to_element(driver.find_element(By.ID, 'password')).click().perform()
    actionChain.send_keys('Qwertyui').perform()
    
    activeTabButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'.rt-tabs .{consts.activeTab}')))
    assert activeTabButton.text == consts.tabTitles[1]

    check_auth_failed(driver, wait)


def test_correct_input_login():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    placeholderInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-input__placeholder'))).text
    assert placeholderInput == consts.placeholderInputsValue[0]

    actionChain.move_to_element(driver.find_element(By.ID, 'username')).click().perform()
    actionChain.send_keys('example_login').perform()

    actionChain.move_to_element(driver.find_element(By.ID, 'password')).click().perform()
    actionChain.send_keys('Qwertyui').perform()
    
    activeTabButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'.rt-tabs .{consts.activeTab}')))
    assert activeTabButton.text == consts.tabTitles[2]

    check_auth_failed(driver, wait)
    

def test_correct_input_ls():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    placeholderInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-input__placeholder'))).text
    assert placeholderInput == consts.placeholderInputsValue[0]

    actionChain.move_to_element(driver.find_element(By.ID, 'username')).click().perform()
    actionChain.send_keys('0123456789012').perform()

    actionChain.move_to_element(driver.find_element(By.ID, 'password')).click().perform()
    actionChain.send_keys('Qwertyui').perform()
    
    activeTabButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'.rt-tabs .{consts.activeTab}')))
    assert activeTabButton.text == consts.tabTitles[3], driver.quit()
    check_auth_failed(driver, wait)


def test_try_auth_with_vk():
    driver, wait = get_driver()

    currentLocale = locale.getlocale()

    old_url = driver.current_url

    wait.until(EC.presence_of_element_located((By.ID, 'oidc_vk'))).click()

    wait.until(lambda driver_lambda: old_url != driver_lambda.current_url 
    and driver.execute_script("return document.readyState == 'complete'"))

    if 'ru_RU' in currentLocale:
        assert wait.until(EC.title_is(consts.vkLoginRu))
    else:
        assert wait.until(EC.title_is(consts.vkLoginEn))
    assert driver.current_url.__contains__('https://oauth.vk.com')

    time.sleep(3)
    driver.quit()


def test_try_auth_with_ok():
    driver, wait = get_driver()

    currentLocale = locale.getlocale()

    old_url = driver.current_url

    wait.until(EC.presence_of_element_located((By.ID, 'oidc_ok'))).click()

    wait.until(lambda driver_lambda: old_url != driver_lambda.current_url 
    and driver.execute_script("return document.readyState == 'complete'"))

    if 'ru_RU' in currentLocale:
        assert wait.until(EC.title_is(consts.okLoginRu))
    else:
        assert wait.until(EC.title_is(consts.okLoginEn))
        assert driver.current_url.__contains__('https://connect.ok.ru')

    time.sleep(3)
    driver.quit()


def test_try_auth_with_mail():
    driver, wait = get_driver()

    currentLocale = locale.getlocale()

    old_url = driver.current_url

    wait.until(EC.presence_of_element_located((By.ID, 'oidc_mail'))).click()

    wait.until(lambda driver_lambda: old_url != driver_lambda.current_url 
    and driver.execute_script("return document.readyState == 'complete'"))

    if 'ru_RU' in currentLocale:
        assert wait.until(EC.title_is(consts.mailLoginRu))
    else:
        assert wait.until(EC.title_is(consts.mailLoginEn))
    assert driver.current_url.__contains__('https://connect.mail.ru/oauth')

    time.sleep(3)
    driver.quit()


def test_try_auth_with_google():
    driver, wait = get_driver()

    old_url = driver.current_url

    wait.until(EC.presence_of_element_located((By.ID, 'oidc_google'))).click()

    wait.until(lambda driver_lambda: old_url != driver_lambda.current_url 
    and driver.execute_script("return document.readyState == 'complete'"))

    assert wait.until(EC.title_contains(consts.googleLogin))
    assert driver.current_url.__contains__('https://accounts.google.com/o/oauth2/auth')

    time.sleep(3)
    driver.quit()

    
def test_try_auth_with_ya():
    driver, wait = get_driver()

    old_url = driver.current_url

    wait.until(EC.presence_of_element_located((By.ID, 'oidc_ya'))).click()

    wait.until(lambda driver_lambda: old_url != driver_lambda.current_url 
    and driver.execute_script("return document.readyState == 'complete'"))

    assert wait.until(EC.title_contains(consts.yaLogin))
    assert driver.current_url.__contains__('https://oauth.yandex.ru/') or driver.current_url.__contains__('https://passport.yandex.ru/auth')

    time.sleep(3)
    driver.quit()


def test_correct_redirect_to_restore_password():
    driver, wait = get_driver()
    
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Забыл пароль'))).click()
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Восстановление пароля'

    driver.quit()


def test_correct_redirect_to_register():
    driver, wait = get_driver()
    
    wait.until(EC.presence_of_element_located((By.ID, 'kc-register'))).click()
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'

    driver.quit()

