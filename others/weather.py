import requests
import datetime
import os
import json



###  IMPORT JSON FILE WITH KEYS/TOKENS ###
tokenkey_path = open("C:\\Users\\Souocare\\Documents\\Projects\\Bot_transportes\\configvars.json")
tokenkey_data = json.loads(tokenkey_path.read())

def get_weather_city(city):
    information = requests.get("http://api.openweathermap.org/data/2.5/weather?q={city}&"
                               "appid={priv_key}&"
                               "units=metric&"
                               "lang=pt".format(city=city,
                                                priv_key=tokenkey_data['Weatherapi_key'])).json()

    if str(information['cod']) == "200":
        metereologia = [tempo["description"].capitalize() for tempo in information["weather"]]
        weather_info = "\n***Neste momento:***\n-> Condição metereológica: {met}\n-> A temperatura é de {t1}, mas que pareçe {t2}. " \
                       "A mínima é de {tmin}, e máxima de {tmax}.\n" \
                       "-> Com uma percentagem de nuvens de {nuv}%.".format(met=' e '.join(metereologia),
                                                                         t1=str(information['main']['temp']),
                                                                         t2=str(information['main']['feels_like']),
                                                                         tmin=str(information['main']['temp_min']),
                                                                         tmax=str(information['main']['temp_max']),
                                                                         nuv=str(information['clouds']['all']))


    elif str(information['cod']) == "404" and str(information['message']) == 'city not found':
        weather_info = "Não foi reconhecida a cidade. Por favor verifique o nome."
    else:
        weather_info = "Não foi possivel obter os dados. Volte a tentar mais tarde."

    return weather_info


def get_weather_geoloc(lat, lon):
    information = requests.get("http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&"
                               "appid={priv_key}&"
                               "units=metric&"
                               "lang=pt".format(lat=lat,
                                                lon=lon,
                                                priv_key="PRIVATE KEY OPENWEATHERAPI")).json()

    if str(information['cod']) == "200":
        print(information)
        metereologia = [tempo["description"].capitalize() for tempo in information["weather"]]
        weather_info = "\n***Neste momento***:\n-> Condição metereológica: {met}\n-> A temperatura é de {t1}, mas que pareçe {t2}. " \
                       "A mínima é de {tmin}, e máxima de {tmax}.\n" \
                       "-> Com uma percentagem de nuvens de {nuv}%.".format(met=' e '.join(metereologia),
                                                                         t1=str(information['main']['temp']),
                                                                         t2=str(information['main']['feels_like']),
                                                                         tmin=str(information['main']['temp_min']),
                                                                         tmax=str(information['main']['temp_max']),
                                                                         nuv=str(information['clouds']['all']))


    elif str(information['cod']) == "404" and str(information['message']) == 'city not found':
        weather_info = "Não foi reconhecida a cidade. Por favor verifique o nome."
    else:
        weather_info = "Não foi possivel obter os dados. Volte a tentar mais tarde."

    return weather_info


def get_forecast_city(city):
    information = requests.get("http://api.openweathermap.org/data/2.5/forecast?q={city}&"
                               "appid={priv_key}&"
                               "units=metric&"
                               "lang=pt".format(city=city,
                                                priv_key="PRIVATE KEY OPENWEATHERAPI")).json()

    temp_min_hoje = 100
    temp_max_hoje = 0
    temp_min_amanha = 100
    temp_max_amanha = 0
    valormin_nuvens_hoje = 100
    valormax_nuvens_hoje = 0
    valormin_nuvens_amanha = 100
    valormax_nuvens_amanha = 0
    metereologia_hoje = []
    metereologia_amanha = []

    data_hoje = datetime.datetime.now()

    print(information)

    for info_weather in information["list"]:
        datetime_weather = datetime.datetime.fromtimestamp(info_weather["dt"])

        if datetime_weather.date() == data_hoje.date():
            if info_weather["main"]["temp_min"] < temp_min_hoje:
                temp_min_hoje = info_weather["main"]["temp_min"]
            if info_weather["main"]["temp_max"] > temp_max_hoje:
                temp_max_hoje = info_weather["main"]["temp_max"]
            for tempo in info_weather["weather"]:
                if (tempo["description"]).capitalize() not in metereologia_hoje:
                    metereologia_hoje.append((tempo["description"]).capitalize())
            if info_weather["clouds"]["all"] < valormin_nuvens_hoje:
                valormin_nuvens_hoje = info_weather["clouds"]["all"]
            if info_weather["clouds"]["all"] > valormax_nuvens_hoje:
                valormax_nuvens_hoje = info_weather["clouds"]["all"]


        elif ((int(datetime_weather.day)) - data_hoje.day) == 1:
            if info_weather["main"]["temp_min"] < temp_min_amanha:
                temp_min_amanha = info_weather["main"]["temp_min"]
            if info_weather["main"]["temp_max"] > temp_max_amanha:
                temp_max_amanha = info_weather["main"]["temp_max"]
            for tempo in info_weather["weather"]:
                if (tempo["description"]).capitalize() not in metereologia_amanha:
                    metereologia_amanha.append((tempo["description"]).capitalize())
            if info_weather["clouds"]["all"] < valormin_nuvens_amanha:
                valormin_nuvens_amanha = info_weather["clouds"]["all"]
            if info_weather["clouds"]["all"] > valormax_nuvens_amanha:
                valormax_nuvens_amanha = info_weather["clouds"]["all"]

        else:
            pass

    if len(metereologia_hoje) != 0:
        info_tempo_hoje = "Para o dia de hoje:\n-> Condições metereológicas possiveis: {met}\n" \
                          "-> Temperatura minima de {tmin} e temperatura máxima de {tmax}\n" \
                          "-> Percentagem minima de nuvens de {nmin}% e máxima de {nmax}%".format(
            met="{} e {}".format(", ".join(metereologia_hoje[:-1]), metereologia_hoje[-1]),
            tmin=temp_min_hoje, tmax=temp_max_hoje,
            nmin=valormin_nuvens_hoje, nmax=valormax_nuvens_hoje)

    else:
        info_tempo_hoje = "O dia está quase no final, por isso só há informações gerais para o dia de amanhã abaixo."

    info_tempo_amanha = "Para o dia de amanhã:\n-> Condições metereológicas possiveis: {met}\n" \
                        "-> Temperatura minima de {tmin} e temperatura máxima de {tmax}\n" \
                        "-> Percentagem minima de nuvens de {nmin}% e máxima de {nmax}%".format(
        met="{} e {}".format(", ".join(metereologia_amanha[:-1]), metereologia_amanha[-1]),
        tmin=temp_min_amanha, tmax=temp_max_amanha,
        nmin=valormin_nuvens_amanha, nmax=valormax_nuvens_amanha)

    return info_tempo_hoje + "\n\n" + info_tempo_amanha




def get_forecast_geoloc(lat, lon):
    information = requests.get("http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&"
                               "appid={priv_key}&"
                               "units=metric&"
                               "lang=pt".format(lat=lat,
                                                lon=lon,
                                                priv_key="PRIVATE KEY OPENWEATHERAPI")).json()

    temp_min_hoje = 100
    temp_max_hoje = 0
    temp_min_amanha = 100
    temp_max_amanha = 0
    valormin_nuvens_hoje = 100
    valormax_nuvens_hoje = 0
    valormin_nuvens_amanha = 100
    valormax_nuvens_amanha = 0
    metereologia_hoje = []
    metereologia_amanha = []

    data_hoje = datetime.datetime.now()

    for info_weather in information["list"]:
        datetime_weather = datetime.datetime.fromtimestamp(info_weather["dt"])

        if datetime_weather.date() == data_hoje.date():
            if info_weather["main"]["temp_min"] < temp_min_hoje:
                temp_min_hoje = info_weather["main"]["temp_min"]
            if info_weather["main"]["temp_max"] > temp_max_hoje:
                temp_max_hoje = info_weather["main"]["temp_max"]
            for tempo in info_weather["weather"]:
                if (tempo["description"]).capitalize() not in metereologia_hoje:
                    metereologia_hoje.append((tempo["description"]).capitalize())
            if info_weather["clouds"]["all"] < valormin_nuvens_hoje:
                valormin_nuvens_hoje = info_weather["clouds"]["all"]
            if info_weather["clouds"]["all"] > valormax_nuvens_hoje:
                valormax_nuvens_hoje = info_weather["clouds"]["all"]


        elif ((int(datetime_weather.day)) - data_hoje.day) == 1:
            if info_weather["main"]["temp_min"] < temp_min_amanha:
                temp_min_amanha = info_weather["main"]["temp_min"]
            if info_weather["main"]["temp_max"] > temp_max_amanha:
                temp_max_amanha = info_weather["main"]["temp_max"]
            for tempo in info_weather["weather"]:
                if (tempo["description"]).capitalize() not in metereologia_amanha:
                    metereologia_amanha.append((tempo["description"]).capitalize())
            if info_weather["clouds"]["all"] < valormin_nuvens_amanha:
                valormin_nuvens_amanha = info_weather["clouds"]["all"]
            if info_weather["clouds"]["all"] > valormax_nuvens_amanha:
                valormax_nuvens_amanha = info_weather["clouds"]["all"]

        else:
            pass

    if len(metereologia_hoje) != 0:
        info_tempo_hoje = "Para o dia de hoje:\n-> Condições metereológicas possiveis: {met}\n" \
                          "-> Temperatura minima de {tmin} e temperatura máxima de {tmax}\n" \
                          "-> Percentagem minima de nuvens de {nmin}% e máxima de {nmax}%".format(
            met="{} e {}".format(", ".join(metereologia_hoje[:-1]), metereologia_hoje[-1]),
            tmin=temp_min_hoje, tmax=temp_max_hoje,
            nmin=valormin_nuvens_hoje, nmax=valormax_nuvens_hoje)

    else:
        info_tempo_hoje = "O dia está quase no final, por isso só há informações gerais para o dia de amanhã abaixo."

    info_tempo_amanha = "Para o dia de amanhã:\n-> Condições metereológicas possiveis: {met}\n" \
                        "-> Temperatura minima de {tmin} e temperatura máxima de {tmax}\n" \
                        "-> Percentagem minima de nuvens de {nmin}% e máxima de {nmax}%".format(
        met="{} e {}".format(", ".join(metereologia_amanha[:-1]), metereologia_amanha[-1]),
        tmin=temp_min_amanha, tmax=temp_max_amanha,
        nmin=valormin_nuvens_amanha, nmax=valormax_nuvens_amanha)

    return info_tempo_hoje + "\n\n" + info_tempo_amanha


def get_all_weather_city(city):
    weather_now = get_weather_city(city)
    weather_after = get_forecast_city(city)

    return weather_now + "\n\n" + weather_after


def get_all_weather_geoloc(lat, lon):
    weather_now = get_weather_geoloc(lat, lon)
    weather_after = get_forecast_geoloc(lat, lon)

    return weather_now + "\n\n" + weather_after
