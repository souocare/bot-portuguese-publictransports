#!/usr/bin/env python3

import telepot, requests, time, pandas as pd
import telepot.namedtuple
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import traceback
import datetime
#functions from files
from metro.menu_metro import metro_option
from metro.menu_metro import get_info_line, get_last_trains, metro_estadolinha, metro_tempocomboio
from ttsl.ttsl import get_option_station, send_ttsl_info
from rl.rl import send_rl_info, rl_partidas_options, get_information_json
from others.piadas_secas import get_piada_seca
from others.weather import get_all_weather_city, get_all_weather_geoloc



#https://telepot.readthedocs.io/en/latest/
bot = telepot.Bot(token='Telegram_Token') #normal



metro_lines = ['Linha Azul', "Linha Amarela", "Linha Verde", "Linha Vermelha",
               "Todas"]

boats_lines = ["Barreiro", "Belém", "Cacilhas", "Cais do Sodre", "Montijo",
               "Porto Brandão", "Seixal", "Terreiro do Paco", "Trafaria"]

sub_options = ["Estado da Linha", "Tempo do próximo comboio"]

lines_metro = ["Aeroporto", "Alameda", "Alfornelos", "Alvalade","Alto Moinhos",
                        "Amadora Este", "Ameixoeira", "Anjos", "Areeiro", "Arroios",
                        "Avenida", "Baixa Chiado", "Bela Vista", "Cabo Ruivo", "Cais Sodré",
                        "Campo Grande", "Campo Pequeno", "Carnide", "Chelas",
                        "Cidade Universitária", "Colégio Militar", "Encarnação", "Entre Campos",
                        "Intendente", "Jardim Zoológico", "Laranjeiras", "Lumiar",
                        "Marquês de Pombal", "Martim Moniz", "Moscavide", "Odivelas",
                        "Olaias", "Olivais", "Oriente", "Parque", "Picoas",
                        "Pontinha", "Praça de Espanha", "Quinta das Conchas", "Rato",
                        "Reboleira", "Restauradores", "Roma", "Rossio", "São Sebastião",
                        "Saldanha", "Santa Apolónia", "Senhor Roubado", "Telheiras",
                        "Terreiro do Paço"]

rl_options = ["Partidas do Infantado", "Partidas do Campo Grande"]

back_options = ["Sair", "Voltar para o Metro", "Voltar para o Menu Principal"]


def mainn_menuu(chatid):
    markup = telepot.namedtuple.ReplyKeyboardMarkup(
        keyboard=[['Metro', "RL"], ["CP", "Carris"], ["Barcos", "Mafrense"], ["Metereologia"]])

    bot.sendMessage(chat_id=chatid,
                    text="Bem-vindo ao teu bot pessoal dos transportes. Escolhe, das opções abaixo,"
                         " qual tu queres ver. \n\nCaso não apareca as opções, basta clicares no simbolo"
                         " que está na barra das mensagens, que é um quadrado com 4 bolinhas lá dentro\n\n"
                         "Caso não queiras nenhuma, podes simplesmente sair da conversa"
                         ", que quando voltares, estarei a tua espera!\n\nPs: Se quiseres uma piada seca, "
                         "escreve 'Piada Seca'\n\n***Warning:*** Eu dependo de que os sites das transportadoras estejam"
                         " funcionais. Por isso se algo não ter, desculpa. Algum problema, "
                         "contacta-me para gonga1999@outlook.pt", reply_markup=markup, parse_mode='Markdown')




if __name__ == '__main__':
    offset = 0
    while True:
        response = bot.getUpdates(offset=offset)

        if len(response) == 0:
            pass
        else:
            try:
                print("Chat ID: " + str(response[0]['message']["chat"]["id"]) +
                  "\nNome: " + str(response[0]['message']["chat"]["first_name"]) + " " + response[0]['message']["chat"]["last_name"] +
                  "\nMensagem: " + str(response[0]['message']['text']) +
                  "\nHoras: " + str(datetime.datetime.fromtimestamp(response[0]['message']['date'])) + "\n")

            except KeyError:
                try:
                    print("Chat ID: " + str(response[0]['message']["chat"]["id"]) +
                          "\nNome: " + str(response[0]['message']["chat"]["first_name"]) +
                          "\nMensagem: " + str(response[0]['message']['text']) +
                          "\nHoras: " + str(datetime.datetime.fromtimestamp(response[0]['message']['date'])) + "\n")

                except KeyError:
                    pass

            try:
                if response[0]['message']['text'] == '/start' \
                        or response[0]['message']['text'] == 'Sim' \
                        or response[0]['message']['text'] == 'Não, quero informações':

                    mainn_menuu(response[0]["message"]['from']['id'])


                elif response[0]['message']['text'] == '/help_commands':
                    all_comands_oldlist = ["Metro", "RL", "CP",
                                           "Carris", "Barcos", "Mafrense", "Metereologia"] + metro_lines + sub_options + boats_lines
                    all_comands_newlist = []
                    for element in all_comands_oldlist:
                        all_comands_newlist.append("-> " + element + "\n")
                    all_commands_str = ''.join(all_comands_newlist)
                    all_commands_str = all_commands_str + "\n-> Escrever o nome da estação para ver o " \
                                                          "tempo de espera (p.e 'Baixa-Chiado')"

                    bot.sendMessage(chat_id=response[0]["message"]['from']['id'],
                                    text="Abaixo estão todos os comandos que pode executar e ter uma resposta mais "
                                         "rapida: \n" + all_commands_str)

                elif response[0]['message']['text'] == 'Metro':
                    metro_option(response, response[0]['message']['from']['id'])
                    # metro_info.metro_option(response, main_menu(response))


                elif response[0]['message']['text'] == 'RL':
                    rl_partidas_options(response[0]['message']['from']['id'])

                elif response[0]['message']['text'] == 'CP':
                    bot.sendMessage(response[0]["message"]['from']['id'], text="Ainda não disponivel.")

                elif response[0]['message']['text'] == 'Carris':
                    bot.sendMessage(response[0]["message"]['from']['id'], text="Ainda não disponivel.")

                elif response[0]['message']['text'] == 'Barcos':
                    get_option_station(response)

                elif response[0]['message']['text'] == 'Mafrense':
                    bot.sendMessage(response[0]["message"]['from']['id'], text="Ainda não disponivel.")
                    
                elif response[0]['message']['text'] == 'Metereologia':
                    bot.sendMessage(response[0]["message"]['from']['id'],
                                    text="Para obter a informação de uma cidade, escreva 'Metereologia - NomeCidade.\n"
                                         "Se preferir, pode simplesmente enviar as suas coordenadas.")

                elif response[0]['message']['text'] == 'Nem por isso' or response[0]['message']['text'] == 'Sim, mais uma!' \
                        or response[0]['message']['text'].lower() == 'piada seca':
                    joke = get_piada_seca()

                    bot.sendMessage(chat_id=response[0]["message"]['from']['id'],
                                    text="Diverte-te com esta piada seca: \n\n{pergunta} \n{resposta}"
                                    .format(pergunta=joke[0], resposta=joke[1]),
                                    reply_markup=telepot.namedtuple.ReplyKeyboardRemove(), parse_mode='markdown')

                    time.sleep(5)

                    markup_anotherjoke = telepot.namedtuple.ReplyKeyboardMarkup(
                        keyboard=[['Sim, mais uma!', "Não, quero informações"]])
                    bot.sendMessage(chat_id=response[0]["message"]['from']['id'],
                                    text="Queres mais uma piada ou nem por isso?", reply_markup=markup_anotherjoke)

                elif response[0]['message']['text'] in sub_options:
                    if response[0]['message']['text'] == 'Estado da Linha':
                        metro_estadolinha(response)
                    elif response[0]['message']['text'] == 'Tempo do próximo comboio':
                        metro_tempocomboio(response)
                    elif response[0]['message']['text'] == 'Voltar para o Menu Principal':
                        mainn_menuu(response[0]['message']['from']['id'])
                    else:
                        pass

                elif response[0]['message']['text'] in lines_metro:
                    if response[0]['message']['text'] == "Sair":
                        mainn_menuu(chatid=response[0]['chat']['id'])

                        offset = offset + 1

                    else:
                        offset_timemetro = get_last_trains(chat_id=response[0]['message']['from']['id'],
                                                           estacao=response[0]['message']['text'],
                                                           query=response)

                        offset = offset_timemetro + 1

                elif response[0]['message']['text'] in metro_lines:
                    if response[0]['message']['text'] == "Todas":
                        offset_estadometro = get_info_line(line="Todas",
                                                           chat_id=response[0]['message']['from']['id'],
                                                           query=response)
                    else:
                        offset_estadometro = get_info_line(line=(response[0]['message']['text']).split(" ")[1],
                                                            chat_id=response[0]['message']['from']['id'],
                                                            query=response)

                    offset = offset_estadometro + 1


                elif response[0]['message']['text'] in boats_lines:
                    offset_ttsl = send_ttsl_info(query=response,
                                                 estacao=response[0]['message']['text'])

                    offset = offset_ttsl + 1

                elif response[0]['message']['text'] in rl_options:
                    offset_rl = send_rl_info(query=response,
                                             partida=response[0]['message']['text'],
                                             horarios=get_information_json())

                    offset = offset_rl + 1


                elif response[0]['message']['text'] in back_options:
                    if response[0]['message']['text'] == "Sair" or response[0]['message']['text'] == "Voltar para o Menu Principal":
                        mainn_menuu(response[0]['message']["chat"]["id"])
                    elif response[0]['message']['text'] == "Voltar para o Metro":
                        metro_option(response, response[0]['message']['from']['id'])
                        
                elif (response[0]['message']['text']).lower().startswith("met - ") or \
                        (response[0]['message']['text']).lower().startswith("met-"):
                    if (response[0]['message']['text']).lower().startswith("met - "):
                        cidade = response[0]['message']['text'][6:]
                    if (response[0]['message']['text']).lower().startswith("met-"):
                        cidade = response[0]['message']['text'][4:]
                    try:
                        bot.sendMessage(chat_id=response[0]["message"]['from']['id'],
                                        text=get_all_weather_city(cidade),
                                        parse_mode='markdown')
                    except:
                        bot.sendMessage(chat_id=response[0]["message"]['from']['id'],
                                        text="De momento não é possivel obter a informação. Tente mais tarde",
                                        parse_mode='markdown')


                else:
                    markup_altern = telepot.namedtuple.ReplyKeyboardMarkup(
                        keyboard=[['Sim'], ["Nem por isso"]])

                    bot.sendMessage(chat_id=response[0]["message"]['from']['id'],
                                    text="Bem-vindo ao teu bot pessoal dos transportes. A tua mensagem para mim foi a "
                                         "seguinte: '{msg}'.\n\n Quiseste começar a conversa para obter informações ou não?"
                                    .format(msg=response[0]['message']['text']), reply_markup=markup_altern)

            except Exception:
                try:
                    location = response[0]['message']['location']
                    bot.sendMessage(chat_id=response[0]["message"]['from']['id'],
                                    text=get_all_weather_geoloc(location['latitude'], location['longitude']),
                                    parse_mode='markdown')

                except:
                    bot.sendMessage(chat_id=response[0]["message"]['from']['id'],
                                    text="De momento não é possivel obter a informação. Tente mais tarde",
                                    parse_mode='markdown')
                    file = open("log_file.txt", "w")
                    file.write(traceback.format_exc())
                    file.close()
                    pass



        if response:
            try:
                offset = response[-1]["update_id"] + 1  # penso que isto é para não receber as mensagens antigas
            except IndexError:
                pass
