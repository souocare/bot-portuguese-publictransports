v#!/usr/bin/env python3

import telepot, requests, time
import telepot.namedtuple
from .metro_information import estado_linha
from .metro_information import dictionary_metro, last_trains_timetable
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

bot = telepot.Bot(token='Telegram_Token') #normal


def metro_option(response, chatid):
    markup_anotherjoke = telepot.namedtuple.ReplyKeyboardMarkup(
        keyboard=[['Estado da Linha', "Tempo do próximo comboio"], ["Voltar para o Menu Principal"]])
    bot.sendMessage(chat_id=chatid,
                    text="Escolha o que queres ver do metro.", reply_markup=markup_anotherjoke)



def get_info_line(line, chat_id, query):
    try:
        bot.sendMessage(chat_id=chat_id, text=estado_linha(line))
    except:
        bot.sendMessage(chat_id=chat_id, text="De momento, não é possivel obter a informação desejada. "
                                              "Tente mais tarde.\nPedimos desculpa.")

    finally:
        return query[0]['update_id']


def get_last_trains(estacao, chat_id, query):
    try:
        text_last_trains = last_trains_timetable(dictionary_metro[estacao])
        while (len(text_last_trains)) == 0:
            text_last_trains = last_trains_timetable(dictionary_metro[estacao])
        #print(text_last_trains)
        bot.sendMessage(chat_id=chat_id, text='{}\nCaso não queira mais, selecione a opção ***Voltar para o Menu Principal*** para voltar ao '
                                              'menu principal, ou ***Voltar para o Metro*** para continuar com informações '
                                              'metro.'.format(text_last_trains), parse_mode='Markdown')
    except:
        bot.sendMessage(chat_id=chat_id,
                        text='De momento, não é possivel obter a informação desejada. '
                             'Tente mais tarde.\nPedimos desculpa.',
                        parse_mode='Markdown')

    finally:
        return query[0]['update_id']

def metro_tempocomboio(query):
    markup_stations = telepot.namedtuple.ReplyKeyboardMarkup(
        keyboard=[['Aeroporto', "Alameda", "Alfornelos", "Alvalade"],
                  ["Alto Moinhos", "Amadora Este", "Ameixoeira", "Anjos"],
                  ["Areeiro", "Arroios", 'Avenida', "Baixa Chiado"],
                  ["Bela Vista", "Cabo Ruivo", "Cais Sodré", "Campo Grande"],
                  ["Campo Pequeno", "Carnide", "Chelas", "Cidade Universitária"],
                  ["Colégio Militar", "Encarnação", "Entre Campos", "Intendente"],
                  ["Jardim Zoológico", "Laranjeiras", "Lumiar", "Marquês de Pombal"],
                  ["Martim Moniz", "Moscavide", "Odivelas", "Olaias"],
                  ["Olivais", "Oriente", "Parque", "Picoas"],
                  ["Pontinha", "Praça de Espanha", "Quinta das Conchas", "Rato"],
                  ["Reboleira", "Restauradores", "Roma", "Rossio"],
                  ["São Sebastião", "Santa Apolónia", "Senhor Roubado", "Telheiras"],
                  ["Terreiro do Paço"], ["Voltar para o Metro", "Voltar para o Menu Principal"]])

    bot.sendMessage(chat_id=query[0]['message']['from']['id'],
                    text='Qual a estação que quer ver os próximos comboios?\n\n ***Selecione a estação que '
                         'pretende nas linhas abaixo apresentadas.*** \n\n '
                         'Se quiser sair, clique em ***Voltar para o Menu Principal***.',
                    parse_mode='Markdown', reply_markup=markup_stations)


def metro_estadolinha(query):
    markup_lines = telepot.namedtuple.ReplyKeyboardMarkup(
        keyboard=[['Linha Azul', "Linha Amarela"], ["Linha Verde", "Linha Vermelha"],
                  ["Todas"], ["Voltar para o Metro", "Voltar para o Menu Principal"]])

    bot.sendMessage(query[0]['message']['chat']['id'], 'Escolha abaixo a linha que quer ver se está disponivel.',
                    reply_markup=markup_lines)
