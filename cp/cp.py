#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import datetime
import os
import requests
# --------------------
#bot modules
import telepot, time
import telepot.namedtuple
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()


ids_startstations = {
    "Sintra": "9461101", "Portela": "9461093", "Algueirão": "9461069", "Mira Sintra - Meleças": "9462042",
    "Mercês": "9461051", "Rio de Mouro": "9461044", "Cacém": "9461002", "Massamá - Barcarena": "9460137",
    "Monte Abraão": "9460111", "Queluz - Belas": "9460103", "Amadora": "9460087", "Reboleira": "9460095",
    "Sta. Cruz / Damaia": "9460038", "Benfica": "9460046", "Alcântara - Terra": "9467025", "Campolide": "9460004",
    "Rossio.": "9459006", "Sete Rios.": "9466076", "Entrecampos.": "9466050", "Roma - Areeiro": "9466035",
    "Marvila": "9466019", "Sta. Apolónia": "9430007", "Braço de Prata": "9431005", "Oriente.": "9431039",
    "Moscavide.": "9431047", "Sacavém.": "9431062", "Bobadela": "9431070", "Santa Iria": "9431112", "Póvoa": "9431146",
    "Alverca": "9431187", "Alhandra": "9431237", "V. F. Xira": "9431278", "Castanheira do Ribatejo": "9431310",
    "Carregado": "9431336", "V. N. Rainha": "9431377", "Espadanal da Azambuja": "9431401", "Azambuja": "9433001",
    "Barreiro.": "9495000", "Barreiro A": "9495026", "Lavradio": "9495042", "Baixa da Banheira": "9495059",
    "Alhos Vedros": "9495075", "Moita": "9495109", "Penteado": "9495125", "Pinhal Novo": "9468007",
    "Venda do Alcaide": "9468049", "Palmela": "9468098", "Setúbal": "9468122", "Praça do Quebedo": "9468130",
    "Praias do Sado A": "9491058", "Penalva": "9417095", "Coina": "9417236",
    "Fogueteiro": "9417186", "Foros de Amora": "9417152", "Corroios": "9417137", "Pragal": "9417087",
    "Cais do Sodré": "9469005", "Santos": "9469013", "Alcântara": "9469039", "Belém.": "9469054",
    "Algés": "9469088", "Cruz Quebrada": "9469104", "Caxias": "9469120", "Paço de Arcos": "9469146",
    "Santo Amaro": "9469161", "Oeiras": "9469179", "Carcavelos": "9469187", "Parede": "9469203", "S. Pedro": "9469229",
    "S. João": "9469237", "Estoril": "9469245", "Monte Estoril": "9469252", "Cascais": "9469260"

}


# functions for bot
bot = telepot.Bot(token=os.getenv('Telegram_Token')) #normal

def get_line_cp(chat_id):
    buttons = telepot.namedtuple.ReplyKeyboardMarkup(
        keyboard=[['Linha de Sintra', "Linha do Sado"],
                  ["Linha da Fertagus", "Linha de Cascais"],
                  ["Voltar para o Menu Principal"]])

    bot.sendMessage(chat_id,
                    text="Escolha qual a opção que deseja ver:", reply_markup=buttons)

def response_estacoes_cp(linha, chat_id):
    if linha == "Linha de Sintra":
        buttons = telepot.namedtuple.ReplyKeyboardMarkup(
            keyboard=[['Sintra', "Portela", "Algueirão"],
                      ["Mercês", "Rio de Mouro", "Mira Sintra - Meleças"],
                      ["Cacém", "Massamá - Barcarena", "Monte Abraão"],
                      ["Queluz - Belas", "Amadora", "Reboleira"],
                      ["Sta. Cruz / Damaia", "Benfica", "Alcântara - Terra"],
                      ["Campolide", "Rossio.", "Sete Rios."],
                      ["Entrecampos.", "Roma - Areeiro", "Marvila"],
                      ["Sta. Apolónia", "Braço de Prata", "Oriente."],
                      ["Moscavide.", "Sacavém.", "Bobadela"],
                      ["Santa Iria", "Póvoa", "Alverca"],
                      ["Alhandra", "V. F. Xira", "Castanheira do Ribatejo"],
                      ["Carregado", "V. N. Rainha", "Espadanal da Azambuja"],
                      ["Azambuja"],
                      ["Voltar para o menu CP / Fertagus", "Voltar para o Menu Principal"]])
    elif linha == "Linha do Sado":
        buttons=telepot.namedtuple.ReplyKeyboardMarkup(
            keyboard=[['Barreiro.', "Barreiro A", "Lavradio"],
                      ["Baixa da Banheira", "Alhos Vedros", "Moita"],
                      ["Penteado", "Pinhal Novo", "Venda do Alcaide"],
                      ["Palmela", "Setúbal", "Praça do Quebedo"],
                      ["Praias do Sado A"],
                      ["Voltar para o menu CP / Fertagus", "Voltar para o Menu Principal"]])
    elif linha == "Linha da Fertagus":
        buttons = telepot.namedtuple.ReplyKeyboardMarkup(
            keyboard=[['Setúbal', "Palmela", "Venda do Alcaide"],
                      ["Pinhal Novo", "Penalva", "Coina"],
                      ["Fogueteiro", "Foros de Amora", "Corroios"],
                      ["Pragal", "Campolide", "Sete Rios."],
                      ["Entrecampos.", "Roma - Areeiro"],
                      ["Voltar para o menu CP / Fertagus", "Voltar para o Menu Principal"]])
    elif linha == "Linha de Cascais":
        buttons=telepot.namedtuple.ReplyKeyboardMarkup(
            keyboard=[['Cais do Sodré', "Santos", "Alcântara"],
                      ["Belém.", "Algés", "Cruz Quebrada"],
                      ["Caxias", "Paço de Arcos", "Santo Amaro"],
                      ["Oeiras", "Carcavelos", "Parede"],
                      ["S. Pedro", "S. João", "Estoril"],
                      ["Monte Estoril", "Cascais"],
                      ["Voltar para o menu CP / Fertagus", "Voltar para o Menu Principal"]])
    else:  # condição não existente
        buttons = telepot.namedtuple.ReplyKeyboardMarkup(
            keyboard=[])
    bot.sendMessage(chat_id,
                    text="Escolha qual a estação que deseja ver:", reply_markup=buttons)





#functions for getting info

def get_onlinedata(partida, datahoras):
    link = "https://www.infraestruturasdeportugal.pt/pt-pt/negocios-e-servicos/horarios/partidas/{id_estacao}/{ano}-" \
           "{mes}-{dia}T{hora}:{min}:{seg}+" \
           "{ano_f}-{mes_f}-{dia_f}T23:59:59".format(id_estacao=ids_startstations[partida], ano='%02d' % datahoras.year,
                                                     mes='%02d' % datahoras.month, dia='%02d' % datahoras.day,
                                                     hora='%02d' % datahoras.hour, min='%02d' % datahoras.minute,
                                                     seg="00", ano_f='%02d' % datahoras.year,
                                                     mes_f='%02d' % datahoras.month, dia_f='%02d' % datahoras.day)


    data = json.loads(requests.get(link).text)

    return data

def get_multiple_data(data):
    prox_comboios = []

    for info in data["HorarioDetalhe"]:
        datahora_comboio = datetime.datetime.strptime(info["HoraPartida"], '%Y-%m-%d %H:%M:%S')
        if info["EstadoComboio"]['Descricao'] == "À tabela":
            informacao_comboio = "Está a horas"
        elif info["EstadoComboio"]['Descricao'] == "SUPRIMIDO":
            informacao_comboio = "Suprimido"
        else:
            informacao_comboio = info["EstadoComboio"]['Descricao']
        texto = "- {origin} ({time}) - {destino} ({operador})-> ***{inform}***".format(origin=info['EstacaoOrigem']['Nome'].capitalize(),
                                                                            time=('%02d' % datahora_comboio.hour) + ":" +
                                                                                 ('%02d' % datahora_comboio.minute),
                                                                            destino=info['EstacaoDestino']['Nome'].capitalize(),
                                                                            inform=informacao_comboio, operador=info['Operador']['Nome'].capitalize())

        if len(prox_comboios) >= 5:
            pass
        else:
            prox_comboios.append(texto)

    return prox_comboios



def get_last_trains_cp(partida, date_from_telegram):
    datahora = datetime.datetime.fromtimestamp(date_from_telegram)
    data = get_onlinedata(partida, datahora)

    if len(data) == 0:
        datahora_amanha = datetime.datetime.strptime("{ano}-{mes}-{dia} 00:00:00".format(ano='%02d' % datahora.year,
                                                                                            mes='%02d' % datahora.month,
                                                                                            dia='%02d' % (datahora.day+1),
                                                                                            hora='%02d' % datahora.hour),
                                              '%Y-%m-%d %H:%M:%S')
        data = get_onlinedata(partida, datahora_amanha)

        next_comboios = get_multiple_data(data)

    elif isinstance(data["HorarioDetalhe"], dict):
        if data["HorarioDetalhe"]["EstadoComboio"]['Descricao'] == "À tabela":
            informacao_comboio = "Está a horas"
        elif data["HorarioDetalhe"]["EstadoComboio"]['Descricao'] == "SUPRIMIDO":
            informacao_comboio = "Suprimido"
        else:
            informacao_comboio = data["HorarioDetalhe"]["EstadoComboio"]['Descricao']
        datahora_comboio = datetime.datetime.strptime(data["HorarioDetalhe"]["HoraPartida"], '%Y-%m-%d %H:%M:%S')
        texto = "- {origin} ({time}) - {destino} ({operador})-> ***{inform}***".format(origin=data["HorarioDetalhe"]['EstacaoOrigem']['Nome'].capitalize(),
                                                                            time=(
                                                                                             '%02d' % datahora_comboio.hour) + ":" +
                                                                                 ('%02d' % datahora_comboio.minute),
                                                                            destino=data["HorarioDetalhe"]['EstacaoDestino']['Nome'].capitalize(),
                                                                            inform=informacao_comboio, operador=data["HorarioDetalhe"]['Operador']['Nome'].capitalize())

        datahora_amanha = datetime.datetime.strptime("{ano}-{mes}-{dia} 00:00:00".format(ano='%02d' % datahora.year,
                                                                                         mes='%02d' % datahora.month,
                                                                                         dia='%02d' % (datahora.day + 1),
                                                                                         hora='%02d' % datahora.hour),
                                                     '%Y-%m-%d %H:%M:%S')
        data = get_onlinedata(partida, datahora_amanha)

        next_comboios = get_multiple_data(data)[:4]
        next_comboios.insert(0, texto)



    else:
        next_comboios = get_multiple_data(data)

    proximos_comboios = "Próximo comboio: \n{first_train}\n\n" \
                        "De seguida:\n{after_train}".format(first_train=next_comboios[0][2:],
                                                            after_train='\n'.join(next_comboios[1:]))
    return proximos_comboios


