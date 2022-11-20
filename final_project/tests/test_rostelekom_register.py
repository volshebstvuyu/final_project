from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

import time

import consts

def get_driver():
    try:
        options = Options()
        options.set_preference('intl.accept_languages', 'en-GB')
        driver = webdriver.Firefox(executable_path = consts.driverPathMozilla, options = options)
    except:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en-GB'})
        driver = webdriver.Chrome(executable_path = consts.driverPathChrome, chrome_options = options)
        
    driver.get(consts.baseUrl)
    driver.maximize_window()    
    wait = WebDriverWait(driver, 40)
    wait.until(EC.presence_of_element_located((By.ID, 'kc-register'))).click()
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'
    
    return driver, wait

def test_register_screen():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    firstNameInput = wait.until(EC.presence_of_element_located((By.NAME, 'firstName')))
    lastNameInput = wait.until(EC.presence_of_element_located((By.NAME, 'lastName')))
    addressNameInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#address')))
    passNameInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password')))
    passConfirmNameInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password-confirm')))

    elementsDictionary = {
        'firstName': firstNameInput,
        'lastName': lastNameInput,
        'address': addressNameInput,
        'password': passNameInput,
        'password-confirm': passConfirmNameInput,
    }
    
    for key in consts.registerKeysDict:
        values = consts.registerKeysDict[key]

        actionChain.click(elementsDictionary[key]).perform()

        for j in range(len(values)):
            actionChain.send_keys(values[j]).perform()
            if key != 'password-confirm':
                driver.find_element(By.XPATH, '//div[@class="rt-select rt-select--search register-form__dropdown"]//input').click()
                time.sleep(1)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.rt-select.rt-select--search.register-form__dropdown div.rt-input__action'))).click()
            else:
                driver.find_element(By.NAME, 'register').click()

            if j < len(values) - 1:
                if key == 'address' and j >= 1:
                    pass
                else:
                    error = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.rt-input-container__meta.rt-input-container__meta--error'))).text

                if key == 'firstName' or key == 'lastName':
                    assert error == consts.registerErrorsName
                elif key == 'address':
                    assert error == consts.registerErrorsAddress
                elif key == 'password':
                    assert error in consts.registerErrorsPassword
                elif key == 'password-confirm':
                    assert error == consts.registerErrorsPasswordConfirm
                    
                time.sleep(1)
                actionChain.double_click(elementsDictionary[key]).click_and_hold().send_keys(Keys.DELETE).perform()
                time.sleep(1)
            else:
                error = wait.until_not(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.rt-input-container__meta.rt-input-container__meta--error')))
                assert error == True

                if key == 'password-confirm':
                    modal = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.card-modal__card')))
                    assert modal != None
            
    driver.quit()
