#!/usr/bin/env python3

import json
import datetime
import telepot, requests, time
import telepot.namedtuple
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import urllib.request
import pandas as pd
from fake_useragent import UserAgent
import os


def get_information_json():
    file = requests.get(
      url="https://raw.githubusercontent.com/souocare/bot-portuguese-publictransports/master/rl/horarios_RL_diretos_infantado.json",
      headers={"Accept": "application/json; charset=utf-8"})

    file.encoding = "ISO 3166-2"

    return file.json()


def get_typeschedule(json, datateste):
    typeschedules = ["Horário Escolar", "Horário Não Escolar", "Horário de Verão"]

    # print(datateste)
    type_final = ""

    for type in typeschedules:
        for sched_set in json[type]['Horário']:
            sched1_obj = datetime.datetime.strptime((sched_set[0]), "%d/%m")
            sched2_obj = datetime.datetime.strptime((sched_set[1]), "%d/%m")

            if sched1_obj <= datateste <= sched2_obj:
                type_final = type_final + type

    return type_final


def rl_partidas_options(chat_id):
    bot = telepot.Bot(token='892727974:AAGJsrqOIt8yqME27WS6R8Np1QOyHzC05fk')

    markup_anotherjoke = telepot.namedtuple.ReplyKeyboardMarkup(
        keyboard=[["Partidas do Infantado", "Partidas do Campo Grande"], ["Voltar para o Menu Principal"]])
    bot.sendMessage(chat_id=chat_id,
                    text="Escolha o que queres ver da Rodoviária de Lisboa.", reply_markup=markup_anotherjoke)


def send_rl_info(query, partida, horarios):
    bot = telepot.Bot(token='892727974:AAGJsrqOIt8yqME27WS6R8Np1QOyHzC05fk')

    bot.sendMessage(query[0]['message']['chat']['id'], text=get_bus(data_from_telegram=query[0]['message']['date'],
                                                                    partida=partida,
                                                                    horarios=horarios), parse_mode='Markdown')

    return query[0]["update_id"]


def get_info_otherweekday(prox_autocarro, dia_semana, autocarros, dados, tipo_horario, partida):
    if dia_semana == "Dias úteis":
        horas = list(dados[tipo_horario][partida]["Sábados"].keys())
        prox_autocarro = prox_autocarro + \
                         "O próximo autocarro é o ***{bus}***\nParte às ***{horas}:{minutos}*** " \
                         "de ***amanhã (sábado)***".format(
                             bus=autocarros[
                                 dados[tipo_horario][partida]["Sábados"][horas[0]][0][1]],
                             horas=horas[0],
                             minutos=dados[tipo_horario][partida]["Sábados"][horas[0]][0][0])
        return prox_autocarro
    else:
        horas = list(dados[tipo_horario][partida]["Dias úteis"].keys())
        prox_autocarro = prox_autocarro + \
                         "O próximo autocarro é o ***{bus}***\nParte às ***{horas}:{minutos}*** de " \
                         "***Segunda-feira***".format(
                             bus=autocarros[
                                 dados[tipo_horario][partida]["Dias úteis"][horas[0]][0][1]],
                             horas=horas[0],
                             minutos=dados[tipo_horario][partida]["Dias úteis"][horas[0]][0][0])
        return prox_autocarro


def get_bus(data_from_telegram, partida, horarios):
    autocarros = {"344": "344 - Direta Bucelas",
                  "354": "354 - Direta Vialonga",
                  "334": "334 - Direta Infantado",
                  "333": "333 - Direta Zambujal", }

    data_hora = datetime.datetime.fromtimestamp(data_from_telegram)

    hora = data_hora.hour
    minuto = data_hora.minute

    dados = horarios

    tipo_horario = get_typeschedule(dados,
                                    datetime.datetime.strptime(str(data_hora.day) + "/" + str(data_hora.month),
                                                               "%d/%m"))

    # print(tipo_horario)

    prox_autocarro = ""

    # https://feriados.com.pt/feriados/portugal/

    dia_semana = ""
    if int(data_hora.weekday()) in [0, 1, 2, 3, 4]:
        dia_semana = dia_semana + "Dias úteis"
    elif int(data_hora.weekday()) == 5:
        dia_semana = dia_semana + "Sábados"
    else:
        dia_semana = dia_semana + "Domingo ou Feriado"

    # print(dia_semana)
    if dia_semana == "Domingo ou Feriado":
        prox_autocarro = prox_autocarro + get_info_otherweekday(prox_autocarro, dia_semana, autocarros, dados,
                                                                tipo_horario, partida)
    else:
        for hora in dados[tipo_horario][partida][dia_semana]:
            if int(hora) == int(data_hora.hour):
                if len(dados[tipo_horario][partida][dia_semana][hora]) != 0:
                    minutos = dados[tipo_horario][partida][dia_semana][hora]
                    for minuto in range(len(minutos)):
                        if format(int(minutos[minuto][0]), "02") > format(int(data_hora.minute), "02") and \
                                format(int(minutos[minuto][0]), "02") == format(int(minutos[0][0]), "02"):
                            prox_autocarro = prox_autocarro + \
                                             "O próximo autocarro é o ***{bus}*** \nParte às ***{horas}:{minutos}***".format(
                                                 bus=autocarros[
                                                     dados[tipo_horario][partida][dia_semana][hora][minuto][
                                                         1]],
                                                 horas=hora,
                                                 minutos=str(format(int(minutos[minuto][0]), "02")))
                            break
                        elif format(int(minutos[minuto - 1][0]), "02") < format(int(data_hora.minute), "02") < \
                                format(int(minutos[minuto][0]), "02"):
                            prox_autocarro = prox_autocarro + \
                                             "O próximo autocarro é o ***{bus}***\nParte às ***{horas}:{minutos}***".format(
                                                 bus=autocarros[
                                                     dados[tipo_horario][partida][dia_semana][hora][minuto][
                                                         1]],
                                                 horas=hora,
                                                 minutos=str(format(int(minutos[minuto][0]), "02")))
                            break

                        elif int(minutos[minuto][0]) < int(data_hora.minute) and int(minutos[minuto][0]) == int(
                                minutos[-1][0]):
                            try:
                                # if len(dados[tipo_horario][partida][dia_semana][str(int(hora)+1)]) != 0:
                                prox_autocarro = prox_autocarro + \
                                                 "O próximo autocarro é o ***{bus}***\nParte às ***{horas}:{minutos}***".format(
                                                     bus=autocarros[
                                                         dados[tipo_horario][partida][dia_semana][
                                                             str(int(hora) + 1)][0][1]],
                                                     horas=str(format(int(hora) + 1, "02")),
                                                     minutos=str(format(int(dados[tipo_horario][partida][dia_semana][
                                                                                str(format(int(hora) + 1, "02"))][0][
                                                                                0]), "02")))

                            except (KeyError, IndexError):
                                if int(data_hora.weekday()) in [4, 5, 6]:
                                    prox_autocarro = prox_autocarro + get_info_otherweekday(prox_autocarro,
                                                                                            dia_semana, autocarros,
                                                                                            dados, tipo_horario,
                                                                                            partida)
                                else:
                                    keys_horario = list(dados[tipo_horario][partida][dia_semana])
                                    prox_autocarro = prox_autocarro + \
                                                     "O próximo autocarro é o ***{bus}*** \nParte amanhã às ***{horas}:{minutos}***".format(
                                                         bus=autocarros[
                                                             dados[tipo_horario][partida][dia_semana][keys_horario[0]][
                                                                 0][1]],
                                                         horas=keys_horario[0],
                                                         minutos=str(format(int(
                                                             dados[tipo_horario][partida][dia_semana][keys_horario[0]][
                                                                 0][0]), "02")))
                                break

                else:
                    try:
                        if len(dados[tipo_horario][partida][dia_semana][str(format(int(hora) + 1, "02"))]) != 0:
                            prox_autocarro = prox_autocarro + \
                                             "O próximo autocarro é o ***{bus}***\nParte às ***{horas}:{minutos}***".format(
                                                 bus=autocarros[
                                                     dados[tipo_horario][partida][dia_semana][
                                                         str(format(int(hora) + 1, "02"))][0][1]],
                                                 horas=str(format(int(hora) + 1, "02")),
                                                 minutos=str(format(int(dados[tipo_horario][partida][dia_semana][
                                                                            str(format(int(hora) + 1, "02"))][0][0]),
                                                                    "02")))
                            break
                        else:
                            if len(dados[tipo_horario][partida][dia_semana][str(format(int(hora) + 2, "02"))]) != 0:
                                prox_autocarro = prox_autocarro + \
                                                 "O próximo autocarro é o ***{bus}***\nPassa às ***{horas}:{minutos}***".format(
                                                     bus=autocarros[
                                                         dados[tipo_horario][partida][dia_semana][
                                                             str(int(hora) + 1)][0][1]],
                                                     horas=str(format(int(hora) + 2, "02")),
                                                     minutos=str(format(int(dados[tipo_horario][partida][dia_semana][
                                                                                str(format(int(hora) + 2, "02"))][0][
                                                                                0]), "02")))
                                break

                            else:
                                prox_autocarro = prox_autocarro + get_info_otherweekday(prox_autocarro, dia_semana,
                                                                                        autocarros, dados, tipo_horario,
                                                                                        partida)
                                break

                    except:
                        prox_autocarro = prox_autocarro + get_info_otherweekday(prox_autocarro, dia_semana, autocarros,
                                                                                dados, tipo_horario, partida)
                        break
            '''
            else:
                if len(dados[tipo_horario][partida][dia_semana][hora]) != 0:
                    print(dia_semana)
                    print(hora)

                    print(dados[tipo_horario][partida][dia_semana][hora][0][1])
                    prox_autocarro = prox_autocarro + \
                                     "O próximo autocarro é o ***{bus}***\nPassa às ***{horas}:{minutos}***".format(
                                         bus=autocarros[
                                             dados[tipo_horario][partida][dia_semana][hora][0][1]],
                                         horas=hora,
                                         minutos=dados[tipo_horario][partida][dia_semana][hora][0][0])
                else:
                    prox_autocarro = prox_autocarro + get_info_otherweekday(prox_autocarro, dia_semana, autocarros,
                                                                            dados, tipo_horario, partida)
                break'''

    if len(prox_autocarro) == 0:
        if int(data_hora.hour) in [0, 1, 2, 3, 4, 5, 6]:
            lista_horas = list(dados[tipo_horario][partida][dia_semana].keys())
            prox_autocarro = prox_autocarro + \
                             "O próximo autocarro é o ***{bus}***\nPassa às ***{horas}:{minutos}***".format(
                                 bus=autocarros[
                                     dados[tipo_horario][partida][dia_semana][
                                         lista_horas[0]][0][1]],
                                 horas=lista_horas[0],
                                 minutos=str(format(int(dados[tipo_horario][partida][dia_semana][
                                                            lista_horas[0]][0][
                                                            0]), "02")))

        elif int(data_hora.hour) == 23:
            lista_horas = list(dados[tipo_horario][partida][dia_semana].keys())
            prox_autocarro = prox_autocarro + \
                             "O próximo autocarro é o ***{bus}***\nPassa amanhã às ***{horas}:{minutos}***".format(
                                 bus=autocarros[
                                     dados[tipo_horario][partida][dia_semana][
                                         lista_horas[0]][0][1]],
                                 horas=lista_horas[0],
                                 minutos=str(format(int(dados[tipo_horario][partida][dia_semana][
                                                            lista_horas[0]][0][
                                                            0]), "02")))

        else:
            prox_autocarro = prox_autocarro + \
                             "Está um autocarro a partir ***agora mesmo*** às ***{horas_now}:{minutos_now}***\n\n" \
                             "Informação para o próximo autocarro às " \
                             "***{horas_next}:{minutos_next}***".format(horas_now=str(data_hora.hour),
                                                                        minutos_now=str(
                                                                            format(int(data_hora.minute), "02")),
                                                                        horas_next=str(data_hora.hour),
                                                                        minutos_next=str(
                                                                            format(int(data_hora.minute) + 1, "02")))
    else:
        pass

    return prox_autocarro
