import json
import tkinter as tk
import tkinter.font
from datetime import datetime
from tkinter import *
from tkinter import ttk

import requests
from PIL import ImageTk, Image


# Date and time update function
def update_clock():
    dtnow = datetime.now()
    datetimelbl.config(text=getmonthbul(dtnow.strftime("%d-%b-%Y %H:%M")))
    window.after(3000, update_clock)


def getmonthbul(input_str):
    months_eng = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    months_bul = ["Яну", "Фев", "Мар", "Апр", "Май", "Юни", "Юли", "Авг", "Сеп", "Окт", "Нов", "Дек"]
    result = input_str
    for i in range(len(months_eng)):
        result = result.replace(months_eng[i], months_bul[i])
    return result


def getweather():
    # Get data from API
    # API Key 9c0da7736675e795326c9c4898312686
    # API URL https://api.openweathermap.org/data/2.5/forecast?q=Burgas,bg&APPID=9c0da7736675e795326c9c4898312686&cnt=6&units=metric
    apicount = 6
    apiurl = "https://api.openweathermap.org/data/2.5/forecast?q=Burgas,bg&APPID=9c0da7736675e795326c9c4898312686&cnt=" + str(
        apicount) + "&units=metric"

    jsonresponse = requests.get(apiurl).text
    weatherinfo = json.loads(jsonresponse)
    # array for labels

    datelabels = []
    templabels = []
    fllabels = []
    preclabels = []
    iconlabels = []

    row_start = 1
    datestrl = ttk.Label(window)
    datestrl.config(text="Дата/час")
    datestrl.grid(row=row_start, column=0, sticky=tk.E)
    tempstrl = ttk.Label(window)
    tempstrl.config(text="Температура")
    tempstrl.grid(row=row_start + 1, column=0, sticky=tk.E)
    flstrl = ttk.Label(window)
    flstrl.config(text="Усеща се")
    flstrl.grid(row=row_start + 2, column=0, sticky=tk.E)
    popstrl = ttk.Label(window)
    popstrl.config(text="Валежи")
    popstrl.grid(row=row_start + 3, column=0, sticky=tk.E)

    for i in range(apicount):
        crow = row_start
        datestring = getmonthbul(datetime.fromtimestamp(weatherinfo["list"][i]["dt"]).strftime("%d-%b %H"))
        temperature = weatherinfo["list"][i]["main"]["temp"]
        feelslike = weatherinfo["list"][i]["main"]["feels_like"]
        precipitation = weatherinfo["list"][i]["pop"]
        wxicon = weatherinfo["list"][i]["weather"][0]["icon"]

        datelabel = ttk.Label(window)
        datelabel.grid(row=crow, column=i + 1, sticky=tk.N)
        datelabel.config(text=datestring + ":00")
        datelabels.append(datelabel)

        crow = crow + 1
        templabel = ttk.Label(window)
        templabel.grid(row=crow, column=i + 1, sticky=tk.N)
        templabel.config(text=str(temperature) + " °C")
        templabels.append(templabel)

        crow = crow + 1
        fllabel = ttk.Label(window)
        fllabel.grid(row=crow, column=i + 1, sticky=tk.N)
        fllabel.config(text=str(feelslike) + " °C")
        fllabels.append(fllabel)

        crow = crow + 1
        preclabel = ttk.Label(window)
        preclabel.grid(row=crow, column=i + 1, sticky=tk.N)
        preclabel.config(text=str(precipitation * 100) + " %")
        preclabels.append(preclabel)

        crow = crow + 1
        path = 'C:\\Users\\35988\\Documents\\Programming\\python\\weathericon\\'
        dimage = Image.open(path + wxicon + "@2x.png")
        dimage = dimage.resize((80, 80), Image.ANTIALIAS);
        tkimage = ImageTk.PhotoImage(dimage)
        iconlabel = ttk.Label(image=tkimage)
        iconlabel.image = tkimage
        iconlabel.grid(row=crow, column=i + 1, sticky=tk.N)
        iconlabels.append(iconlabel)


window = tk.Tk()
window.geometry("640x480")
window.resizable(width=False, height=False)
window.title('Weather App')

# Configure UI
dfont = tkinter.font.nametofont("TkDefaultFont")
dfont.config(size=9)
dfont.config(family="Verdana")

for row_num in range(window.grid_size()[1]):
    window.rowconfigure(row_num, pad=5)

# Label for date and time
datetimelbl = ttk.Label(window)
datetimelbl.grid(column=0, row=0, sticky=tk.N, padx=5, columnspan=9)
datetimelbl.config(font=("Verdana", 14))
update_clock()
getweather()

window.mainloop()
