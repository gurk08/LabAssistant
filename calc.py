#импорт нужных библиотек
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import base64
import matplotlib
import os

matplotlib.use('Agg')

# Объявление констант 
c = 299792458  # Скорость света
h = 6.626e-34  # Постоянная Планка

def analyze_spectrum(filename):
    try:
        plt.clf()
        x, y = np.loadtxt(filename, unpack=True)

        # Поиск максимальной интенсивности
        max_index = np.argmax(y)  # Возвращает индекс максимального элемента
        resonance_position = x[max_index]

        # Ширина на полувысоте
        half_max = y[max_index] / 2
        left_index = np.argmin(np.abs(y[:max_index] - half_max))
        right_index = np.argmin(np.abs(y[max_index:] - half_max)) + max_index
        FWHM = x[right_index] - x[left_index]

        # Построение графика
        plt.plot(x, y)
        plt.axvline(resonance_position, color='red', linestyle='--', label="Положение резонанса")
        plt.hlines(half_max, x[left_index], x[right_index], linestyle='--',color='green', label="Ширина на полувысоте")

        plt.xlabel("Длина волны в нанометрах")
        plt.ylabel("Интенсивность")
        plt.title("Спектр с отмеченным пиком и его шириной на полувысоте")
        plt.legend()

        plt.savefig("files/spectrum_plot.png", format='png')

        # Формирование сообщения для чат-бота
        message = f"Положение резонанса: {round(resonance_position,2)}\nШирина на полувысоте: {round(FWHM,2)}\n\n"
        plot = open('files/spectrum_plot.png', 'rb')
        os.remove('files/spectrum.txt')
        return message, plot


    except Exception as e:
        return f"Ошибка при обработке файла: {e}"


'''
Видимый свет: 400-700 нм
Ультрафиолетовый свет (УФ): 10-400 нм
Инфракрасный свет (ИК): 700 нм - 1 мм
Микроволны: 1 мм - 1 м
Радиоволны: > 1 м
''' 
#Функции для перевода величин 
def frequency_to_wavelen(freq):
    return  "{:.2e}".format(c / freq) 
def frequency_to_enph(freq):
    return "{:.2e}".format(freq*h)
def wavelen_to_frequency(wavelen):
    return "{:.2e}".format(c/wavelen)
def wavelen_to_enph(wavelen):
    freq = c/wavelen
    return "{:.2e}".format(freq*h)
def enph_to_wavelen(enph):
    freq = enph/h
    return "{:.2e}".format(c/freq)
def enph_to_frequency(enph):
    freq = enph/h
    return "{:.2e}".format(freq)

#Определение диапазон волн, измерение в нм
def rangewaves(wavelen):
    if wavelen >= 1e9:
        return "Это радиоволна"
    elif wavelen >= 1e6:
        return "Это радиоволна"
    elif wavelen >= 1e3:
        return "Это радиоволна"
    elif wavelen >= 1e2:
        return "Это радиоволна"
    elif wavelen >= 10:
        return "Это радиоволна"
    elif wavelen >= 700:
        return "Это инфракрасный свет"
    elif wavelen >= 400:
        return "Это видимый свет" 
    elif wavelen >= 10:
        return "Это ультрафиолетовый свет"
    elif wavelen >= 0.01:
        return "Это рентгеновское излучение"
    else:
        return "Это гамма-излучение" 




