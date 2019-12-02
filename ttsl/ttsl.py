#!/usr/bin/env python3

import telepot, requests, time
import telepot.namedtuple
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import urllib.request, json
import pandas as pd
from fake_useragent import UserAgent

bot = telepot.Bot(token='892727974:AAGJsrqOIt8yqME27WS6R8Np1QOyHzC05fk')

def get_option_station(query):
    markup_lines = telepot.namedtuple.ReplyKeyboardMarkup(
        keyboard=[['Barreiro', "Belém", "Cacilhas"], ["Cais do Sodré", "Montijo", "Porto Brandão"],
                  ["Seixal", "Terreiro do Paco", "Trafaria"], ["Voltar para o Menu Principal"]])

    bot.sendMessage(query[0]['message']['chat']['id'], 'Escolha a estação que quer ver a informação.',
                    reply_markup=markup_lines)

def send_ttsl_info(query, estacao):
    dictionary_boats = {
        "Barreiro": 16,
        "Belém": 8,
        "Cacilhas": 6,
        "Cais do Sodre": 5,
        "Montijo": 2,
        "Porto Brandão": 10,
        "Seixal": 3,
        "Terreiro do Paco": 15,
        "Trafaria": 9
    }


    bot.sendMessage(query[0]['message']['chat']['id'], text=get_info_ttsl(dictionary_boats[estacao]), parse_mode='Markdown')
    return query[0]["update_id"]


def get_info_ttsl(station):
    try:
        response = requests.get("https://ttsl.pt/").text

        partidasnonce = response[response.find("partidasNonce") + 16:response.find("partidasNonce") + 26]

        ua = UserAgent()

        req = urllib.request.Request("https://ttsl.pt/wp-admin/admin-ajax.php")

        req.add_header("Connection", "keep-alive")
        req.add_header("Accept", "*/*")
        req.add_header("Origin", "https://ttsl.pt")
        req.add_header("X-Requested-With", "XMLHttpRequest")
        req.add_header("User-Agent", ua.ie)
        req.add_header("Sec-Fetch-Mode", "cors")
        req.add_header("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
        req.add_header("Sec-Fetch-Site", "same-origin")
        req.add_header("Referer", "https://ttsl.pt/")
        req.add_header("Accept-Encoding", "gzip, deflate, br")
        req.add_header("Accept-Language", "pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7")
        req.add_header("Cookie", "cookiebanner=1")

        body = b"action=partidasAjax-submit&terminal=id_terminal&partidasNonce=pnonce".replace(b"id_terminal", bytes(str(station), encoding='utf-8')).replace(b"pnonce", bytes(partidasnonce, encoding='utf-8'))

        response = urllib.request.urlopen(req, body)

        data = response.read()
        json_website_data = json.loads(data.decode(response.info().get_content_charset('utf-8')))

        datatable_ttsl = (pd.read_html(json_website_data['html'])[0])
        data_ttsl_list = ["Próximo barco:".format(), "\nBarcos a seguir:"]

        for row in range(len(datatable_ttsl)):
            dados = [datatable_ttsl.iloc[row]['Partida'][
                     datatable_ttsl.iloc[row]['Partida'].index('Partida: ') + len('Partida: '):],
                     datatable_ttsl.iloc[row]['Destino'][
                     datatable_ttsl.iloc[row]['Destino'].index('Destino: ') + len('Destino: '):],
                     datatable_ttsl.iloc[row]['Estado'][
                     datatable_ttsl.iloc[row]['Estado'].index('Estado: ') + len('Estado: '):]]

            try:
                dados.append(
                    datatable_ttsl.iloc[row]['Sala'][datatable_ttsl.iloc[row]['Sala'].index('Sala: ') + len('Sala: '):])
            except:
                dados.append("a determinar")

            if datatable_ttsl.iloc[row].equals(datatable_ttsl.iloc[0]):
                data_ttsl_list.insert(1, "-> O barco das ***{horas}*** com destino a "
                                         "***{destino}*** tem o estado de '***{estado}***' "
                                         "e na sala ***{sala}***.".format(horas=dados[0], destino=dados[1],
                                                                          estado=dados[2], sala=dados[3]))
            else:
                data_ttsl_list.append("-> O barco das ***{horas}*** com destino a "
                                      "***{destino}*** tem o estado de '***{estado}***' "
                                      "e na sala ***{sala}***.".format(horas=dados[0], destino=dados[1],
                                                                       estado=dados[2], sala=dados[3]))

        #print(data_ttsl_list)
        return '\n'.join(data_ttsl_list[:6])

    except:
        return "De momento, não é possivel obter a informação desejada. Tente mais tarde.\nPedimos desculpa."


