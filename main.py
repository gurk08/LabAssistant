#импорт нужных библиотек
import telebot
import calc
from telebot import types
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib
import logging
matplotlib.use('Agg')

bot = telebot.TeleBot('ТОКЕН') #тут содержится токен, который выдал BotFather
dev_id = 111111111 #тут содержится id разработчика, которому на прямую прийдет обратная связь


media_dir = 'files'

#создание кнопок
translation_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton('1️⃣')
btn2 = types.KeyboardButton('2️⃣')
btn3 = types.KeyboardButton('3️⃣')
btn4 = types.KeyboardButton('4️⃣')
btn5 = types.KeyboardButton('5️⃣')
btn6 = types.KeyboardButton('6️⃣')
translation_markup.add(btn1, btn2, btn3,btn4,btn5,btn6) 



acts_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
btn12 = types.KeyboardButton('❶')
btn22 = types.KeyboardButton('❷')
btn32 = types.KeyboardButton('❸')
btn42 = types.KeyboardButton('❹')
acts_markup.add(btn12, btn22, btn32,btn42)

user_state = {} # словарь для хранения выбора пользователя

#начало работы
@bot.message_handler(commands=['start'])
def start(message):
    user_state[message.chat.id] = {"method": None, "profile": None, "shape": None}
    bot.send_message(message.from_user.id, 
                          text=f"Привет! 👋 Я твой ассистент для научных задач. Я могу помогать тебе с:\n"
                               f" ❶ Переводом различных физических величин\n"
                               f" ❷ Анализом спектров.\n"
                               f" ❸ Вычислением флюенса лазерной системы\n"
                               f" ❹ Отправкой обратной связи разработчику\n"
                               f"Что вы хотите сделать сейчас? 🤔\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)
#обработка всех команд
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '❶':
        bot.send_message(message.from_user.id, "Какой именно перевод хотите сделать?", parse_mode='Markdown')
        bot.send_message(message.from_user.id, 
                          text=f"1️⃣Частота излучения --> Длина волны\n"
                               f"2️⃣Длина волны --> Частота излучения\n"
                               f"3️⃣Длина волны --> Энергия фотона\n"
                               f"4️⃣Энергия фотона --> Длина волны\n"
                               f"5️⃣Энергия фотона --> Частота излучения\n"
                                f"6️⃣Частота излучения --> Энергия фотона\n"
                               f"Выберите цифру, которая соотвествует номеру нужной вам операции ",reply_markup=translation_markup)
    elif message.text == '❷':
        bot.send_message(message.from_user.id, "Прикрепите файл в формате txt, где каждая точка спектра - отдельная строчка, длина волны (пробел или таб) интенсивность", parse_mode='Markdown',reply_markup=None)
        bot.register_next_step_handler(message, handle_file)
    elif message.text == '1️⃣':
        bot.send_message(message.from_user.id, "Введите частоту излучения в Герцах", parse_mode='Markdown',reply_markup=None)
        bot.send_message(message.from_user.id, "Вводите целые числа или десятичные дроби. В качестве разделятеля используйте символ точки", parse_mode='Markdown',reply_markup=None)
        bot.register_next_step_handler(message, handle_frequency_to_wavelen)
    elif message.text == '2️⃣':
        bot.send_message(message.from_user.id, "Введите длину волны в метрах", parse_mode='Markdown',reply_markup=None)
        bot.send_message(message.from_user.id, "Вводите целые числа или десятичные дроби. В качестве разделятеля используйте символ точки", parse_mode='Markdown',reply_markup=None)
        bot.register_next_step_handler(message, handle_wavelen_to_frequency)
    elif message.text == '3️⃣':
        bot.send_message(message.from_user.id, "Введите длину волны в метрах", parse_mode='Markdown',reply_markup=None)
        bot.send_message(message.from_user.id, "Вводите целые числа или десятичные дроби. В качестве разделятеля используйте символ точки", parse_mode='Markdown',reply_markup=None)
        bot.register_next_step_handler(message, handle_wavelen_to_enph)
    elif message.text == '4️⃣':
        bot.send_message(message.from_user.id, "Введите энергию фотона в Джоулях", parse_mode='Markdown',reply_markup=None)
        bot.send_message(message.from_user.id, "Вводите целые числа или десятичные дроби. В качестве разделятеля используйте символ точки", parse_mode='Markdown',reply_markup=None)
        bot.register_next_step_handler(message, handle_enph_to_wavelen)
    elif message.text == '5️⃣':
        bot.send_message(message.from_user.id, "Введите энергию фотона в Джоулях", parse_mode='Markdown',reply_markup=None)
        bot.send_message(message.from_user.id, "Вводите целые числа или десятичные дроби. В качестве разделятеля используйте символ точки", parse_mode='Markdown',reply_markup=None)
        bot.register_next_step_handler(message, handle_frequency_to_enph)
    elif message.text == '6️⃣':
        bot.send_message(message.from_user.id, "Введите частоту излучения в Герцах", parse_mode='Markdown',reply_markup=None)
        bot.send_message(message.from_user.id, "Вводите целые числа или десятичные дроби. В качестве разделятеля используйте символ точки", parse_mode='Markdown',reply_markup=None)
        bot.register_next_step_handler(message, handle_frequency_to_enph)
    elif message.text == '❸':
        try:
            user_state[message.chat.id]["method"] = None
            user_state[message.chat.id]["profile"] = None
            user_state[message.chat.id]["shape"] = None
            choose_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            choose_markup.add("Средняя мощность", "Энергия импульса")
            bot.send_message(message.chat.id, "По какому параметру рассчитать флюенс?", reply_markup=choose_markup)
            bot.register_next_step_handler(message, choose_method_fluence) 
        except KeyError as e:
            logging.error(f"KeyError in user_state: {e}")
            bot.send_message(chat_id=message.chat.id, text="Что-то пошло не так. Нажмите сюда: /start")
    elif message.text == '❹':
        bot.send_message(message.chat.id, "Расскажите, что вам нравится в боте, а что ещё можно  улучшить",reply_markup=None)
        bot.register_next_step_handler(message, feedback) 
# Обработчики для ввода величин:
def handle_frequency_to_wavelen(message):
    global freq 
    try:
        freq = float(message.text)
        res = calc.frequency_to_wavelen(freq)
        bot.send_message(message.from_user.id, f"Длинна волны: {str(res)} нанометров")
        bot.send_message(message.from_user.id, calc.rangewaves(float(res)))
        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)

    except ValueError:
        bot.send_message(message.from_user.id, "Посчитать не удалось.")
        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)
def handle_frequency_to_enph(message):
    global freq 
    try:
        freq = float(message.text)
        res = str(calc.frequency_to_enph(freq))
        bot.send_message(message.from_user.id, f"Энергия фотона: {res} джоулей")
        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)

    except ValueError:
        bot.send_message(message.from_user.id, "Посчитать не удалось")
        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)
def handle_enph_to_wavelen(message):
    global enph
    try:
        enph = float(message.text)
        res = str(calc.enph_to_wavelen(enph))
        bot.send_message(message.from_user.id, f"Длинна волны: {res} нанометров")
        bot.send_message(message.from_user.id, calc.rangewaves(float(res)))
        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)

    except ValueError:
        bot.send_message(message.from_user.id, "Посчитать не удалось")
        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)
def handle_enph_to_frequency(message):
    global enph
    try:
        enph = float(message.text)
        res = calc.enph_to_frequency(enph)
        bot.send_message(message.from_user.id, f"Частота излучения: {res} герц")
        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)

    except ValueError:
        bot.send_message(message.from_user.id, "Посчитать не удалось")
        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)
def handle_wavelen_to_frequency(message):
    global wavelen
    try:
        wavelen = float(message.text)
        res = calc.wavelen_to_frequency(wavelen)
        bot.send_message(message.from_user.id, f"Частота излучения: {res} герц")
        bot.send_message(message.from_user.id, calc.rangewaves(float(wavelen)))
        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)

    except ValueError:
        bot.send_message(message.from_user.id, "Посчитать не удалось")
        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)
def handle_wavelen_to_enph(message):
    global wavelen
    try:
        wavelen = float(message.text)
        res = calc.wavelen_to_enph(wavelen)
        bot.send_message(message.from_user.id, f"Энергия фотона: {res} джоулей")
        bot.send_message(message.from_user.id, calc.rangewaves(float(wavelen)))
        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)

    except ValueError:
        bot.send_message(message.from_user.id, "Посчитать не удалось")
        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)
        
# Код для анализа спектра
def handle_file(message):
    if message.document:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(os.path.join(media_dir, 'spectrum.txt'), 'wb') as f:
            f.write(downloaded_file)

        result_message,plot= calc.analyze_spectrum("files/spectrum.txt")
        bot.send_message(message.from_user.id, result_message,reply_markup=acts_markup)
        bot.send_photo(message.from_user.id, photo=plot)
        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)
        


# Обработка выбора метода для флюенса
def choose_method_fluence(message):
    a = message.text
    user_state[message.chat.id]["method"] = a
    
    bot.send_message(message.chat.id, "Какой профиль у лазера?")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Гауссовский", "Плоский")
    bot.send_message(message.chat.id, "Выберите вариант:", reply_markup=markup)
    bot.register_next_step_handler(message, choose_profile_fluence) 

# Обработка выбора профиля для флюенса
def choose_profile_fluence(message):
    user_state[message.chat.id]["profile"] = message.text
    if message.text == "Гауссовский" and user_state[message.chat.id]["method"] == "Энергия импульса":
        bot.send_message(message.chat.id, "Введите диаметр луча (в мм) и энергию импульса (в мДж) через пробел. В десятичной дроби в качестве разделителя используйте точку")
        bot.register_next_step_handler(message, handle_gauss_fluence1)
    elif message.text == "Гауссовский" and user_state[message.chat.id]["method"] == "Средняя мощность":
        bot.send_message(message.chat.id, "Введите диаметр луча (в мм), среднюю мощность (в Вт) и частоту следования импульсов(в Гц) через пробел. В десятичной дроби в качестве разделителя используйте точку")
        bot.register_next_step_handler(message, handle_gauss_fluence2)
    elif message.text == "Плоский":
        bot.send_message(message.chat.id, "Какая форма у луча?")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Круглый", "Прямоугольный", "Эллипс")
        bot.send_message(message.chat.id, "Выберите вариант:", reply_markup=markup)
        bot.register_next_step_handler(message, choose_shape_fluence)

# Обработка выбора формы для плоского луча
def choose_shape_fluence(message):
    user_state[message.chat.id]["shape"] = message.text
    bot.send_message(message.chat.id, "Введите параметры:\n"
                                      "  - Круг: диаметр (мм)\n"
                                      "  - Прямоугольник: ширина (мм) высота (мм)\n"
                                      "  - Эллипс: большая ось (мм) малая ось (мм)\n"
                                      "В десятичной дроби в качестве разделителя используйте точку")
    
    bot.register_next_step_handler(message, handle_flat_fluence)

# Обработка ввода данных для Гауссовского профиля
def handle_gauss_fluence1(message):
    try:
        data = message.text.split()
        diameter = float(data[0])
        energy = float(data[1])
        fluence = (2 * energy) / (3.14159 * (diameter / 2)**2)
        area = 3.14159 * (diameter / 2)**2
        bot.send_message(message.chat.id, f"Флюенс: {fluence:.2f} Дж/см²")
        bot.send_message(message.chat.id, f"Площадь пятна: {area:.2f} см²")
        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы.\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)

    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат ввода. Пожалуйста, введите числа через пробел.")
        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)

def handle_gauss_fluence2(message):
    try:
        data = message.text.split()
        diameter = float(data[0])/10
        pow = float(data[1])
        freq = float(data[2])
        energy = pow//freq
        area = 3.14159 * (diameter / 2)**2
        fluence = (2 * energy) / (3.14159 * (diameter / 2)**2)
        bot.send_message(message.chat.id, f"Флюенс: {fluence:.2f} Дж/см²")
        bot.send_message(message.chat.id, f"Площадь пятна: {area:.2f} см²")
        bot.send_message(message.chat.id, f"Энергия импульса: {energy:.2f} Дж²")


        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)

    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат ввода. Пожалуйста, введите числа через пробел")



# Обработка ввода данных для Плоского профиля
def handle_flat_fluence(message):
    try:
        data = message.text.split()
        method = user_state[message.chat.id]["method"]
        shape = user_state[message.chat.id]["shape"]
        if shape == "Круглый":
            diameter = float(data[0])
            area = 3.14159 * (diameter / 2)**2
        elif shape == "Прямоугольный":
            width = float(data[0])
            height = float(data[1])
            area = width * height
        elif shape == "Эллипс":
            major_axis = float(data[0])
            minor_axis = float(data[1])
            area = 3.14159 * (major_axis / 2) * (minor_axis / 2)
        if user_state[message.chat.id]["method"]== "Энергия импульса":
            user_state[message.chat.id]["area"] = area/100  # Сохраняем площадь в user_state
            bot.send_message(message.chat.id, "Введите энергию импульса (в мДж).В десятичной дроби в качестве разделителя используйте точку")
            bot.register_next_step_handler(message, handle_calc_flat_fluence1)  # Вызываем handle_calc_flat_fluence1
        elif user_state[message.chat.id]["method"] == "Средняя мощность":
            user_state[message.chat.id]["area"] = area/100  # Сохраняем площадь в user_state
            bot.send_message(message.chat.id, "Введите среднюю мощность (в Вт) и частоту импульсов (в Гц) через пробел. В десятичной дроби в качестве разделителя используйте точку")
            bot.register_next_step_handler(message, handle_calc_flat_fluence2)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат ввода. Пожалуйста, введите числа через пробел")



def handle_calc_flat_fluence1(message):
    try:
        area = user_state[message.chat.id]["area"]
        data = message.text.split()
        energy = float(data[0])/1000
        fluence = energy /area
        bot.send_message(message.chat.id, f"Флюенс: {fluence:.2f} Дж/см²")
        bot.send_message(message.chat.id, f"Площадь пятна: {area:.2f} см²")
        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)

    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат ввода. Пожалуйста, введите числа через пробел")
        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)


def handle_calc_flat_fluence2(message):
    try:
        area = user_state[message.chat.id]["area"]
        data = message.text.split()
        pow = float(data[0])
        freq = float(data[1])
        energy = pow/freq
        fluence = energy /area
        bot.send_message(message.chat.id, f"Флюенс: {fluence:.2f} Дж/см²")
        bot.send_message(message.chat.id, f"Площадь пятна: {area:.2f} см²")
        bot.send_message(message.chat.id, f"Энергия импульса: {energy:.2f} Дж²")

        bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
        bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)

    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат ввода. Пожалуйста, введите числа через пробел")

def feedback(message):
    feedback_text = f"Отзыв от @{message.from_user.username} ({message.from_user.first_name} {message.from_user.last_name}):\n\n{message.text}"
    bot.send_message(dev_id, feedback_text) # Отправка обратной связи вам
    bot.send_message(message.chat.id, "Спасибо за ваш отзыв! 👍")
    bot.send_message(message.from_user.id, "Что я еще могу сделать для вас ?",reply_markup=acts_markup)
    bot.send_message(message.from_user.id, 
                          text=f" ❶ Перевод физических величин\n"
                               f" ❷ Анализ спектров\n"
                               f" ❸ Вычисление флюенса лазерной системы\n"
                               f" ❹ Отправить обратную связь разработчику\n"
                               f"Выберите соответствующую цифру\n",reply_markup=acts_markup)


if __name__ == '__main__':
   bot.polling(non_stop = True) 