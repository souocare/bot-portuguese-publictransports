#!/usr/bin/env python3

import requests, re, datetime

dictionary_metro = {"Aeroporto":"AP", "Alameda":"AM", "Alfornelos":"AF", "Alvalade":"AL","Alto Moinhos": "AH",
                        "Amadora Este":"AS", "Ameixoeira":"AX", "Anjos":"AN", "Areeiro":"AE", "Arroios":"AR",
                        "Avenida":"AV", "Baixa Chiado":"BC", "Bela Vista":"BV", "Cabo Ruivo":"CR", "Cais Sodré":"CS",
                        "Campo Grande":"CG", "Campo Pequeno":"CP", "Carnide": "CA", "Chelas":"CH",
                        "Cidade Universitária":"CU", "Colégio Militar":"CM", "Encarnação":"EN", "Entre Campos":"EC",
                        "Intendente":"IN", "Jardim Zoológico": "JZ", "Laranjeiras": "LA", "Lumiar": "LU",
                        "Marquês de Pombal": "MP", "Martim Moniz": "MM", "Moscavide": "MO", "Odivelas": "OD",
                        "Olaias": "OL", "Olivais": "OS", "Oriente": "OR", "Parque": "PA", "Picoas": "PI",
                        "Pontinha": "PO", "Praça de Espanha": "PE", "Quinta das Conchas": "QC", "Rato": "RA",
                        "Reboleira": "RB", "Restauradores": "RE", "Roma": "RM", "Rossio": "RO", "São Sebastião": "SS",
                        "Saldanha": "SA", "Santa Apolónia": "SP", "Senhor Roubado": "SR", "Telheiras": "TE",
                        "Terreiro do Paço": "TP", "Voltar para Metro":"Voltar para Metro",
                        "Voltar para Menu Principal":"Voltar para Menu Principal"}


## Important Functions for requests of Metro API
def get_access_token():
    headers_get_token= {
        'Authorization': 'PRIVATE Metro API TOKEN HERE',
    }

    data_get_token = {
      'grant_type': 'password',
      'username': 'INSER_USERNAME_HERE',
      'password': 'INSER_PASSWORD_HERE'
    }

    response_get_token = requests.post('https://api.metrolisboa.pt:8243/token',
                                       headers=headers_get_token, data=data_get_token, verify=False).json()

    return response_get_token["access_token"]

def response_json(link):
    headers_get_information = {
        'accept': 'application/json',
        'Authorization': "Bearer {}".format(get_access_token()),
    }

    response_json = requests.get('https://api.metrolisboa.pt:8243/estadoServicoML/1.0.1' + link,
                                 headers=headers_get_information, verify=False).json()

    return response_json


## Main Functions
def estado_linha(linha):
    if linha == "Todas":
        resposta_todos = response_json('/estadoLinha/todos')
        linhas = ["amarela", "azul", "verde", "vermelha"]
        text_estado_todas_linhas = ""

        for linha in linhas:
            if resposta_todos["resposta"][linha.lower()] == " Ok":
                text_estado_todas_linhas = text_estado_todas_linhas + "A linha {} está a funcionar corretamente.\n".format(linha)
            else:
                text_estado_todas_linhas = text_estado_todas_linhas + "A linha {} está com problemas. O problema é: {}\n".format(linha,
                                                                                         get_line_problem("linha " + linha,
                                                                                                          resposta_todos["resposta"]))
        return text_estado_todas_linhas

    else:
        #sendo choices a escolha da linha
        resposta_linha = response_json('/estadoLinha/{}'.format(linha))
        if resposta_linha["resposta"][linha.lower()] == " Ok":
            return "A linha {} está a funcionar sem problemas.".format(linha)
        else:
            return "A linha está com problemas. O problema é: \n{}".format(
                                                                        get_line_problem(linha, resposta_linha))


def last_trains_timetable(estacao):

    last_stations = {60:"Aeroporto", 38:"S. Sebastião", 54:"Cais do Sodré", 50:"Telheiras", 43:"Odivelas",
                48:"Rato", 33:"Reboleira", 42:"Santa Apolónia"}

    #print("estacao: ", estacao)

    #print(response_json("/tempoEspera/Estacao/{}".format(estacao)))

    resposta_tempo = ''

    for item in response_json("/tempoEspera/Estacao/{}".format(estacao))["resposta"]:
        resposta_tempo = resposta_tempo + "Os próximos comboios com destino final ***{d_final}*** são: \n" \
               "***Tempo de Chegada 1:*** {tp1} minutos\n***Tempo de Chegada 2:*** {tp2} minutos\n" \
               "***Tempo de Chegada 3:*** {tp3} minutos\n\n".format(d_final=last_stations[int(item['destino'])],
                                                          tp1=str(datetime.timedelta(seconds=int(item['tempoChegada1']))),
                                                          tp2=str(datetime.timedelta(seconds=int(item['tempoChegada2']))),
                                                          tp3=str(datetime.timedelta(seconds=int(item['tempoChegada3']))))
    return resposta_tempo



## Secondary functions to use in the main ones
def get_line_problem(linha, resposta):
    abrv = {"amarela":"am", "azul":"az", "verde":"vd", "vermelha":"vm"}
    return resposta["resposta"]["tipo_msg_" + abrv[linha.split()[1]]]