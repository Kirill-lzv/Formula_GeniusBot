import os
from background import keep_alive
import telebot
from telebot import types
TOKEN = os.environ['TOKEN']

formuls_math = [i.strip().split(':') for i in open('formuls/math.txt', 'r')]
len_formuls_math = len(formuls_math)
formuls_phys = [i.strip().split(':') for i in open('formuls/phys.txt', 'r')]
len_formuls_phys = len(formuls_phys)
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id, 'Здравствуй. Выбери нужный тебе предмет!', reply_markup=keyboard())


@bot.message_handler(content_types=['text'])
def send_text(message):
  if message.text == '➗ Математика':
    req = bot.send_message(message.chat.id, 'Напиши название нужной тебе формулы')
    # print(k, 123)
    bot.register_next_step_handler(req, find_in_db_math)
    # print(1)
  elif message.text == '🧑‍🔬 Физика':
    mess = bot.send_message(message.chat.id, 'Напиши название нужной тебе формулы')
    # print(k, 123)
    bot.register_next_step_handler(mess, find_in_db_phys)
    
  else:
    bot.send_message(message.chat.id, 'Выберите предмет из списка', reply_markup=keyboard())
    
    
    #из input по ключу достать значение из БД

def find_in_db_math(message):
  c = 0
  for i in formuls_math:
    c += 1
    # print(i, 2)
    # print(message.text, 3)
    # print(i[0], i[1], 4)
    if message.text.lower() == i[0]:
      # print(i[0], 0)
      bot.send_message(message.chat.id, i[1], reply_markup=keyboard())
      break
    elif c == len_formuls_math:
      req = bot.send_message(message.chat.id, 'Формула не найдена. Попробуйте написать по-другому', reply_markup=keyboard())
      bot.register_next_step_handler(req, find_in_db_math)


def find_in_db_phys(message):
  c = 0
  for i in formuls_phys:
    c += 1
    if message.text.lower() == i[0]:
      # print(i[0], 0)
      bot.send_message(message.chat.id, i[1], reply_markup=keyboard())
      break
    elif c == len_formuls_phys:
      mess = bot.send_message(message.chat.id, 'Формула не найдена. Попробуйте написать по-другому', reply_markup=keyboard())
      bot.register_next_step_handler(mess, find_in_db_phys)
        


def keyboard():
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  btn1 = types.KeyboardButton('➗ Математика')
  btn2 = types.KeyboardButton('🧑‍🔬 Физика')
  markup.add(btn1, btn2)
  return markup

keep_alive()
bot.infinity_polling(none_stop=True)