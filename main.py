import json
import tkinter as tk
import tkinter.font
from tkinter import messagebox
from datetime import datetime
from tkinter import *
from tkinter import ttk

import requests


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
    for j in range(len(datelabels)):
        datelabels[j].destroy()
        templabels[j].destroy()
        fllabels[j].destroy()
        preclabels[j].destroy()

    datelabels.clear()
    templabels.clear()
    fllabels.clear()
    preclabels.clear()

    apicount = 8
    apiurl = "https://api.openweathermap.org/data/2.5/forecast?q=Burgas,bg&APPID=9c0da7736675e795326c9c4898312686&cnt=" + str(
        apicount) + "&units=metric"

    jsonresponse = requests.get(apiurl).text
    weatherinfo = json.loads(jsonresponse)

    col_start = 0
    crow = 1

    datestrl = ttk.Label(window)
    datestrl.config(text="Дата/час")
    datestrl.grid(row=crow, column=col_start, sticky=tk.E)
    datelabels.append(datestrl)
    tempstrl = ttk.Label(window)
    tempstrl.config(text="Температура")
    tempstrl.grid(row=crow, column=col_start+1, sticky=tk.E)
    templabels.append(tempstrl)
    flstrl = ttk.Label(window)
    flstrl.config(text="Усеща се")
    flstrl.grid(row=crow, column=col_start+2, sticky=tk.E)
    fllabels.append(flstrl)
    popstrl = ttk.Label(window)
    popstrl.config(text="Валежи")
    popstrl.grid(row=crow, column=col_start+3, sticky=tk.E)
    preclabels.append(popstrl)

    crow += 1
    for i in range(apicount):
        datestring = getmonthbul(datetime.fromtimestamp(weatherinfo["list"][i]["dt"]).strftime("%d-%b %H"))
        temperature = weatherinfo["list"][i]["main"]["temp"]
        feelslike = weatherinfo["list"][i]["main"]["feels_like"]
        precipitation = weatherinfo["list"][i]["pop"]

        datelabel = ttk.Label(window)
        datelabel.grid(row=crow+i, column=col_start, sticky=tk.N)
        datelabel.config(text=datestring + ":00")
        datelabels.append(datelabel)

        templabel = ttk.Label(window)
        templabel.grid(row=crow+i, column=col_start+1, sticky=tk.N)
        templabel.config(text=str(temperature) + " °C")
        templabels.append(templabel)

        fllabel = ttk.Label(window)
        fllabel.grid(row=crow+i, column=col_start+2, sticky=tk.N)
        fllabel.config(text=str(feelslike) + " °C")
        fllabels.append(fllabel)

        preclabel = ttk.Label(window)
        preclabel.grid(row=crow+i, column=col_start+3, sticky=tk.N)
        preclabel.config(text=str(round(precipitation * 100)) + " %")
        preclabels.append(preclabel)

    window.after(120000,getweather)

# arrays for the labels
datelabels = []
templabels = []
fllabels = []
preclabels = []

window = tk.Tk()
window.geometry("640x480")
window.resizable(width=False, height=False)
window.config(bg="#e6f542")
window.title('Weather App')
style = ttk.Style(window)
style.configure("TLabel",background="#e6f542")
style.configure("TLabel",padding="5")

# Configure UI
dfont = tkinter.font.nametofont("TkDefaultFont")
dfont.config(size=12)
dfont.config(family="Verdana")


# Label for date and time
datetimelbl = ttk.Label(window)
datetimelbl.grid(column=0, row=0, sticky=tk.N, padx=5, columnspan=9)
datetimelbl.config(font=("Verdana", 18))
update_clock()
getweather()

window.mainloop()
