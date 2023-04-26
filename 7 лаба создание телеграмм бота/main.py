import telebot
import psycopg2
from telebot import types
import datetime

conn = psycopg2.connect(database="telebase",
                        user="postgres",
                        password="erjgi58fl8iflu",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()
token = '5759186669:AAH5vRz-Uxal24yYcmjKNyg281EIesC5BC8'
bot = telebot.TeleBot(token)
days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
times = ['9:30-11:05', '11:20-12:55', '13:10-14:45', '15:25-17:00', '17:15-18:50']


def show_timetable(message, day):
    subjects = {"9:30": "Нет пары", "11:20": "Нет пары", "13:10": "Нет пары", "15:25": "Нет пары", "17:15": "Нет пары"}
    cursor.execute("SELECT * FROM timetable WHERE day=%s", (str(day),))
    records = list(cursor.fetchall())
    for i in records:
        cursor.execute("SELECT * FROM teacher WHERE subject=%s", (str(i[2]),))
        records = list(cursor.fetchall())
        teacher = records[0][1]
        subjects[i[4]] = i[2] + "\n" + i[3] + '\n' + teacher
    bot.send_message(message.chat.id, days[int(day.split('.')[1]) - 1])
    bot.send_message(message.chat.id, '----------------------')
    for i in range(1, 6):
        bot.send_message(message.chat.id, str(i) + '. ' + times[i - 1])
        bot.send_message(message.chat.id, subjects[times[i - 1].split('-')[0]])
    bot.send_message(message.chat.id, '----------------------')


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Понедельник", "Вторник", "Среда")
    keyboard.row("Четверг", "Пятница", "Суббота")
    keyboard.row("Расписание на текущую неделю", "Расписание на следующую неделю")
    bot.send_message(message.chat.id, 'Привет! Здесь вы можете узнать своё расписание', reply_markup=keyboard)
    bot.send_message(message.chat.id, 'Чтобы узнать расписание напишите интересующий вас день или неделю')
    bot.send_message(message.chat.id, 'или воспользуйтесь кнопками')


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я умею:')
    bot.send_message(message.chat.id, 'Выдавать расписание на конкретный день')
    bot.send_message(message.chat.id, 'Выдавать расписание на конкретную неделю')
    bot.send_message(message.chat.id, 'Указать какая сейчас неделя при помощи команды /week')
    bot.send_message(message.chat.id, 'Дать ссылку на сайт МТУСИ при помощи команды /mtuci')


@bot.message_handler(commands=['week'])
def start_message(message):
    week = str(datetime.date.today() - datetime.date(2023, 1, 30)).split(' ')[0]
    week = int(week) // 7 + 1
    if week % 2 == 0:
        info = 'Чётная'
    else:
        info = 'Нечётная'
    bot.send_message(message.chat.id, 'Сейчас {} неделя, {}'.format(week, info))


@bot.message_handler(commands=['mtuci'])
def start_message(message):
    bot.send_message(message.chat.id, 'официальный сайт МТУСИ – https://mtuci.ru/')


@bot.message_handler(content_types=['text'])
def answer(message):
    week = str(datetime.date.today() - datetime.date(2023, 1, 30)).split(' ')[0]
    week = int(week) // 7 + 1
    if message.text.lower() == "понедельник":
        show_timetable(message, str(week % 2) + '.' + '1')
    elif message.text.lower() == "вторник":
        show_timetable(message, str(week % 2) + '.' + '2')
    elif message.text.lower() == "среда":
        show_timetable(message, str(week % 2) + '.' + '3')
    elif message.text.lower() == "четверг":
        show_timetable(message, str(week % 2) + '.' + '4')
    elif message.text.lower() == "пятница":
        show_timetable(message, str(week % 2) + '.' + '5')
    elif message.text.lower() == "суббота":
        show_timetable(message, str(week % 2) + '.' + '6')
    elif message.text.lower() == "расписание на текущую неделю":
        bot.send_message(message.chat.id, 'Расписание на текущую неделю:')
        if week % 2 == 1:
            week = 1
        for i in range(1, 7):
            show_timetable(message, str(week % 2) + '.' + str(i))
    elif message.text.lower() == "расписание на следующую неделю":
        bot.send_message(message.chat.id, 'Расписание на следующую неделю:')
        week += 1
        if week % 2 == 0:
            week = 2
        for i in range(1, 7):
            show_timetable(message, str(week) + '.' + str(i))
    else:
        bot.send_message(message.chat.id, 'Извините, я Вас не понял.')


bot.infinity_polling()
