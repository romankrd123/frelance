import telebot
from telebot import types
import sqlite3
import random



bot = telebot.TeleBot('5552582819:AAEGcTghEs-5jkP9WAZYNQabMXWP7qT0aO0')
@bot.message_handler(commands=['start'])

def welcome(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("стать экспертом")
    item2 = types.KeyboardButton("найти эксперта")
    item3 = types.KeyboardButton("я эксперт")
    item4 = types.KeyboardButton("поставить лайк")
    item5 = types.KeyboardButton("БАГ!!!")
    markup.add(item1, item2, item3, item4, item5)

    bot.send_message(message.chat.id, "Привет, тут ты можешь получить услугу или сам стать экспертом", reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def lalala(message):
    #подключение к бд
    expert = ''
    db = sqlite3.connect('database.db')
    cursor.execute("""CREATE TABLE IF NOT EXISTS expenses(
    rey INT,
    name TEXT,
    zan TEXT,
    pro TEXT,
    like INT,
    )""")
    if message.chat.type == 'private':
        #Если смс = стать экспертом
        if message.text == 'стать экспертом':
            bot.send_message(message.chat.id, 'Введите свой nikname, {0.first_name}, в формате: @nikname, а через запятую введите тему, по которой Вы будете работать'.format(message.from_user))

        #если смс = найти эксперта
        elif message.text == 'найти эксперта':
            bot.send_message(message.chat.id, 'Введите тему, по которой Вы ищите эксперта')
        # если смс = я эксперт
        elif message.text == 'я эксперт':
            bot.send_message(message.chat.id, 'Введите nikname')
            if '@' in message.text[0]:
                if message.text in expert:
                    bot.send_message(message.chat.id, 'ok')
        #если смс = поставить лайк
        elif message.text == 'поставить лайк':
            bot.send_message(message.chat.id, 'Введите nikname, а затем введите через запятую слово "лайк"')
        #Если нашли баг
        elif message.text == 'БАГ!!!':
            bot.send_message(message.chat.id, 'Почта: krd569812@gmail.com')
        else:

            if '@' in message.text[0]:
                    expert = message.text
                    expert = expert.replace(' ','')
                    experts = expert.split(',')
                    zan = experts[-1]
                    print(expert.split(','))
                    cursor = db.cursor()
                    #поставить лайк
                    if cursor.execute("SELECT name FROM expenses WHERE name == ?", (f'{experts[0]}',)).fetchone() != None and zan.upper() == 'ЛАЙК':
                        for i in cursor.execute(f"SELECT like FROM expenses WHERE name == '{experts[0]}'"):
                            like = i[0]
                        cursor.execute(f'UPDATE expenses SET like = {1 + like} WHERE name = "{experts[0]}"')
                        db.commit()
                    #вход в аккаунт
                    elif cursor.execute("SELECT name FROM expenses WHERE name == ?", (f'{experts[0]}',)).fetchone() != None and zan.upper() != 'ЛАЙК':
                        db.row_factory = sqlite3.Row
                        
                        cursor.execute("SELECT id FROM expenses WHERE name == ?", (f'{experts[0]}',))
                        x = experts[-1]
                        xs = cursor.fetchone()
                        x = f'({x},)'
                        if str(x) == str(xs):
                            bot.send_message(message.chat.id, 'Вы вошли в аккаунт')
                            db.close()
                    #Создание профеля
                    elif cursor.execute("SELECT name FROM expenses WHERE name == ?", (f'{experts[0]}',)).fetchone() == None:
                        password = random.randint(100000000, 999999999)
                        query = f" INSERT INTO expenses (id, name, zan, like, pro) VALUES({password}, '{experts[0]}', '{zan.upper()}', 0, 'нет') "
                        cursor.execute(query)
                        db.commit()
                        db.close()
                        bot.send_message(message.chat.id, f'Вы зарегистрированны, Ваш пароль: {password}')
                    elif cursor.execute("SELECT name FROM expenses WHERE name == ?", (f'{experts[0]}',)).fetchone() != None:
                        bot.send_message(message.chat.id, "Пользователь с таким nikname'ом ужеесть")
                    
                
                
            else:
                db.row_factory = sqlite3.Row
                cursor = db.cursor()
                zan= message.text
                if None == cursor.execute("SELECT name FROM expenses WHERE zan == ?", (f'{zan.upper()}',)).fetchone():
                    bot.send_message(message.chat.id, 'Нет спецалиста')
                else:
                    cursor.execute(f"SELECT * FROM expenses WHERE zan == '{zan.upper()}'")
                    #x = cursor.fetchall()
                    #x.split(',')
                    for x in cursor:
                        bot.send_message(message.chat.id, f"nikname: {x['name']}, про: {x['pro']}, лайки: {x['like']}")
    

bot.polling(none_stop=True)
