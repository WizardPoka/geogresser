import telebot
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

# Создаем экземпляр телеграм-бота
bot = telebot.TeleBot("7152606441:AAEY0jELuQNAiLj9D2Nf50x8npFBq04caBs")

# Глобальная переменная для отслеживания состояния входа
is_logged_in = False

# Создаем экземпляр драйвера браузера
options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
options.add_argument('--headless')  # Запуск браузера в фоновом режиме (без графического интерфейса)
driver = webdriver.Chrome(options=options)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот для получения ссылки на игру в GeoGuessr. Используйте команду /go для входа в аккаунт и начала игры. Введите URL карты:")

# Обработчик команды /go
@bot.message_handler(commands=['go'])
def go(message):
    global is_logged_in
    if not is_logged_in:
        # Заходим на страницу входа
        driver.get("https://www.geoguessr.com/signin/")

        # Адрес электронной почты и пароль
        mail = "palhamberg@gmail.com"
        passw = "Ispilkeren73"

        # Находим поле для ввода электронной почты и вводим почту
        email_field = driver.find_element("name", "email")
        email_field.send_keys(mail)
        email_field.send_keys(Keys.TAB)

        # Находим поле для ввода пароля и вводим пароль
        password_field = driver.find_element("name", "password")
        password_field.send_keys(passw)
        password_field.send_keys(Keys.ENTER)

        time.sleep(1)
        is_logged_in = True
        bot.send_message(message.chat.id, "Вы успешно вошли в аккаунт.")
    else:
        bot.send_message(message.chat.id, "Вы уже вошли в аккаунт.")

# Обработчик команды /stop
@bot.message_handler(commands=['stop'])
def stop(message):
    global is_logged_in
    if is_logged_in:
        driver.quit()  # Закрываем браузер
        is_logged_in = False
        bot.send_message(message.chat.id, "Вы успешно вышли из аккаунта и закрыли браузер.")
    else:
        bot.send_message(message.chat.id, "Вы еще не вошли в аккаунт.")

# Обработчик всех текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global is_logged_in
    if is_logged_in:
        map_url = message.text
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

        bot.send_message(message.chat.id, link_value)
    else:
        bot.send_message(message.chat.id, "Сначала войдите в аккаунт с помощью команды /go.")

# Запускаем бота
bot.delete_webhook(drop_pending_updates=True)
bot.polling()
