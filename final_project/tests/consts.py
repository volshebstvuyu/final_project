driverPathChrome = 'driver/chromedriver.exe'
driverPathMozilla = 'driver/geckodriver.exe'
baseUrl = 'https://b2c.passport.rt.ru'
activeTab = 'rt-tab--active'
tabButtonsId = ['t-btn-tab-phone', 't-btn-tab-mail', 't-btn-tab-login', 't-btn-tab-ls']
placeholderInputsValue = ['Мобильный телефон', 'Электронная почта', 'Логин', 'Лицевой счёт']
tabTitles = ['Телефон', 'Почта', 'Логин', 'Лицевой счёт']
sendedKeys = ['79160123456', 'test@test.ru', 'someText', '012345678901']
sendedKeyCaptcha = 'Qwe1asd'
registerFormKeysFirstName = ['Е', 'Ее']
registerFormKeysLastName = ['Е', 'Ее']
registerFormKeysAddress = ['Е', '+79999999999', 'test@test.ru']
registerFormPassword = ['а', 'аааааааа', 'pechenka', 'pechenka1', 'Pechenka89']
registerFormPasswordConfirm = ['Pechenka12', 'Pechenka89']

registerKeysDict = {
    'firstName': registerFormKeysFirstName, 
    'lastName': registerFormKeysLastName,
    'address': registerFormKeysAddress,
    'password': registerFormPassword,
    'password-confirm': registerFormPasswordConfirm
}

registerErrorsName = 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
registerErrorsAddress = 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'
registerErrorsPassword = [
    'Длина пароля должна быть не менее 8 символов',
    'Пароль должен содержать только латинские буквы',
    'Пароль должен содержать хотя бы 1 спецсимвол или хотя бы одну цифру',
    'Пароль должен содержать хотя бы одну заглавную букву'
]
registerErrorsPasswordConfirm = 'Пароли не совпадают'


googleLogin = 'Google Аккаунты'
yaLogin = 'Авторизация'

vkLoginEn = 'VK | Login'
okLoginEn = 'OK'
mailLoginEn = 'Mail.Ru — Access request'

vkLoginRu = 'ВКонтакте | Вход'
okLoginRu = 'Одноклассники'
mailLoginRU = 'Mail.Ru — Запрос доступа'