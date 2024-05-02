from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

# Адрес электронной почты и пароль
mail = "palhamberg@gmail.com"
passw = "Ispilkeren73"

# Создаем экземпляр драйвера браузера
options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
options.add_argument('--headless')  # Запуск браузера в фоновом режиме (без графического интерфейса)
driver = webdriver.Chrome(options=options)

# Заходим на страницу входа
driver.get("https://www.geoguessr.com/signin/")

# Находим поле для ввода электронной почты и вводим почту
email_field = driver.find_element("name", "email")
email_field.send_keys(mail)
email_field.send_keys(Keys.TAB)

# Находим поле для ввода пароля и вводим пароль
password_field = driver.find_element("name", "password")
password_field.send_keys(passw)
password_field.send_keys(Keys.ENTER)

time.sleep(1)

while True:
    map_url = input("Введите URL карты: ")
    map_url += "/play"
    driver.get(map_url)
    time.sleep(1)

    challenge_button = driver.find_element("xpath", "//img[@alt='Challenge']")
    actions = ActionChains(driver)
    actions.move_to_element(challenge_button).click().perform()
    time.sleep(0.5)

    invite_friends_button = driver.find_element("xpath", "//button[@data-qa='invite-friends-button']")
    invite_friends_button.click()
    time.sleep(1)

    link_field = driver.find_element("name", "copy-link")
    link_value = link_field.get_attribute("value")

    print(link_value)
