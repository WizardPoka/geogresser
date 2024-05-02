# ====================================================================================

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# import app.handlers.keyboards as kb

user_router = Router()

# Глобальная переменная для отслеживания состояния входа
is_logged_in = False

# Создаем экземпляр драйвера браузера
options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
options.add_argument('--headless')  # Запуск браузера в фоновом режиме (без графического интерфейса)
driver = webdriver.Chrome(options=options)

# ====================================================================================
 
# Обработчик команды /start
@user_router.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Я бот для получения ссылки на игру в GeoGuessr. Используйте команду /go для входа в аккаунт и начала игры. Введите URL карты:")

# Обработчик команды /go
@user_router.message(Command("go"))
async def go(message: Message):
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
        await message.answer("Вы успешно вошли в аккаунт.")
    else:
        await message.answer("Вы уже вошли в аккаунт.")

# # Обработчик команды /stop
# @user_router.message_handler(commands=['stop'])
# async def stop(message: Message):
#     global is_logged_in
#     if is_logged_in:
#         driver.quit()  # Закрываем браузер
#         is_logged_in = False
#         user_router.send_message(message.chat.id, "Вы успешно вышли из аккаунта и закрыли браузер.")
#     else:
#         user_router.send_message(message.chat.id, "Вы еще не вошли в аккаунт.")

# Обработчик всех текстовых сообщений
@user_router.message()
async def echo_all(message: Message):
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

        await message.answer(link_value)
    else:
        await message.answer("Сначала войдите в аккаунт с помощью команды /go.")


# ====================================================================================

@user_router.message(Command("help"))
async def get_help(message: Message):
    await message.answer("Команда /help")


