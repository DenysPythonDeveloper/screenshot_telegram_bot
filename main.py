import telebot
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def comm_start(message):
    bot.send_message(message.chat.id, 'Привет, я Бот-скриншотер😄\n'
                                      'Скинь мне ссылку сайта и я сделаю скрин🖨')


@bot.message_handler(commands=['help'])
def comm_help(message):
    bot.send_message(message.chat.id, 'Вот тебе пример ссылки:\n'
                                      '"https://www.google.com/"')


@bot.message_handler(content_types=['text'])
def take_screenshot(message):
    message_url = str(message.text)
    if message_url.startswith('https') or message_url.startswith('http'):
        bot.send_message(message.chat.id, 'Одну секунду, делаю скрин...')
        d_cap = dict(DesiredCapabilities.PHANTOMJS)
        d_cap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 "
            "Safari/537.36")
        browser = webdriver.PhantomJS(desired_capabilities=d_cap)
        browser.get(f'{message.text}')
        browser.set_window_size(1920, 1080)
        element = browser.find_element_by_tag_name('body')
        element.screenshot("screenshot.png")
        browser.quit()
        bot.send_message(message.chat.id, 'Вот, держи свой скрин!⬇')
        bot.send_document(message.chat.id, open('./screenshot.png', 'rb'))
    else:
        bot.send_message(message.chat.id,
                         'Неа, ссылка должна начинатся с "https"\n'
                         'Попробуй еще раз😋\n'
                         'Если не выйдет, тогда жми сюда→/help')


bot.polling()
