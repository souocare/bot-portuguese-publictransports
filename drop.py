#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dropbox
import json
import datetime
import os
from dropbox.files import WriteMode
from dotenv import load_dotenv

load_dotenv()

dbx = dropbox.Dropbox(os.getenv('Dropbox_key'))

def get_data_fromdropbox(ficheiro):
    a, d = dbx.files_download(ficheiro)

    json_data = json.loads(d.content.decode("ISO-8859-1"))

    return json_data

def updatefile_dropbox(data, ficheiro):
    jsontostr = json.dumps(data)
    strtobytes = bytes(jsontostr.encode())
    #jsontobytes = bytes(json.dumps(data))

    dbx.files_upload(strtobytes, ficheiro, WriteMode.overwrite)

def check_chatid(chatid, name):
    data = get_data_fromdropbox("/Users.json")
    chats_ids = data.keys()

    if chatid not in chats_ids:
        data[chatid] = name
        updatefile_dropbox(data, "/Users.json")
        return "Guardado no ficheiro."
    else:
        return "Já existe no ficheiro."
        pass

def get_sugestion(chatid, phrase, date):
    sugestion = phrase[9:]
    data = get_data_fromdropbox("/Sugestions.json")
    data[str(datetime.datetime.fromtimestamp(date))] = [str(chatid), sugestion]
    updatefile_dropbox(data, "/Sugestions.json")

