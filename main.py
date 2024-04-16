from tkinter import *
from tkinter import ttk
import requests
from PIL import Image, ImageTk


city_name = ""
temp = ""
temp_feels_like = ""
conditions = ""


def weather(city):
    s_city = city
    city_id = 501175
    # Тут пишется ваш API OPEN WEATHER:
    appid = ""

    # Определяется название и id города:
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                     params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        # print("city:", cities)
        # print('city_id=', city_id)

        global city_name
        city_name = cities

        city_id = data['list'][0]['id']
    except Exception as e:
        print("Exception (find):", e)
        pass

    # Определяется температура и климатическиме условия:
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()

        global temp
        global temp_feels_like
        global conditions
        temp = data['main']['temp']
        temp_feels_like = data['main']['feels_like']
        conditions = data['weather'][0]['description']

        # print("conditions:", data['weather'][0]['description'])
        # print("temp:", data['main']['temp'])
        # print("temp_feels_like:", data['main']['feels_like'])
        # print("temp_min:", data['main']['temp_min'])
        # print("temp_max:", data['main']['temp_max'])
    except Exception as e:
        print("Exception (weather):", e)
        pass

# Первоначальная инициализация интерфейса:
root = Tk()
root["bg"] = "chartreuse2"
root.title("Погода")
root.geometry('340x180')
root.resizable(width=False, height=False)
root.config(bg="skyblue")

bg_rain = Image.open("bg_rain.png").resize((340, 180))
bg_pc = Image.open("bg_partly_cloudy.png").resize((340, 180))
bg_hc = Image.open("bg_half_cloudy.png").resize((340, 180))
bg_mc = Image.open("bg_mainly_cloudy.png").resize((340, 180))
bg_clear = Image.open("bg_clear.png").resize((340, 180))
bg_main = Image.open("bg_main.png").resize((340, 180))

bg = ImageTk.PhotoImage(bg_main)
bg_lab = Label(root, image=bg)
entrance_lab = Label(text="Введите город или населённый пункт", fg='black', font=("Arial Bold", 14))
weather_show_but = Button(text=f"Показать погоду")
temp_lab = Label(fg='black', text=f"Температура:")
temp_feels_like_lab = Label(fg='black', text=f"Ощущается как:")
cond_lab = Label(fg='black', text=f"Осадки:")

# Функция вывода погоды:
def weather_show(event):
    s = str(entrance.get())
    weather(s)
    temp_lab['text'] = f'Температура: {temp}'
    cond_lab['text'] = f'Осадки: {conditions}'
    temp_feels_like_lab['text'] = f'Ощущается как: {temp_feels_like}'
    if conditions == 'дождь' or conditions == 'небольшой дождь':
        bg = ImageTk.PhotoImage(bg_rain)
    elif conditions == 'облачно с прояснениями':
        bg = ImageTk.PhotoImage(bg_pc)
    elif conditions == 'переменная облачность':
        bg = ImageTk.PhotoImage(bg_hc)
    elif conditions == 'пасмурно':
        bg = ImageTk.PhotoImage(bg_mc)
    else:
        bg = ImageTk.PhotoImage(bg_clear)
    bg_lab["image"] = bg
    bg_lab.update()
    root.mainloop()

# Запуск программы:
weather_show_but.bind('<Button-1>', weather_show)

entrance_lab.place(x=5, y=10)
entrance = ttk.Entry()
entrance.place(width=165, x=2, y=48)
weather_show_but.place(x=170, y=45)
temp_lab.place(x=0, y=80)
temp_feels_like_lab.place(x=0, y=100)
cond_lab.place(x=0, y=120)
bg_lab.pack(side="top", fill="both")

root.mainloop()
