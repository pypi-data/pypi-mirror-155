#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/20 11:40
# @Author  : lj
# @File    : data_from.py
import datetime
def data_format_():
    us_month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October','November', 'December']

    spanish_month = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre','noviembre', 'diciembre']
    s_spanish_month = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre','Noviembre', 'Diciembre']

    french_month = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre','novembre', 'décembre']
    s_french_month = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre','Novembre', 'Décembre']

    italy_month = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre','ottobre', 'novembre', 'dicembre']
    s_italy_month = ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre','Ottobre', 'Novembre', 'Dicembre']

    danish_month = ['januar', 'februar', 'märz', 'april', 'mai', 'juni', 'juli', 'august', 'september', 'oktober', 'noviembre', 'dezember']
    s_danish_month = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'Noviembre', 'Dezember']



    month = {}
    register_list = [
        spanish_month,
        s_spanish_month,
        french_month,
        s_french_month,
        italy_month,
        s_italy_month,
        danish_month,
        s_danish_month,
    ]
    for i,v in enumerate(us_month):
        a = month[v] = []
        for register in register_list:
            a.append(register[i])
    return month

def data_format(time):
    time = time.replace(' de ', ' ')
    time = time.replace('.', '')
    time = time.replace(',', '')
    month = data_format_()
    is_j = True
    for i in month:
        if i in time:
            is_j = False
    if is_j:
        for k, v in month.items():
            for i in v:
                if i in time:
                    time = time.replace(i, k)
                    break


    time = time.split(' ')

    try:
        int(time[0])
    except Exception:
        time[0], time[1] = time[1], time[0]
    time = ' '.join(time)

    try:
        time_format = datetime.datetime.strptime(time, '%d %b %Y')
    except Exception:
        time_format = datetime.datetime.strptime(time, '%d %B %Y')
    data_time = datetime.datetime.strftime(time_format, '%Y-%m-%d')
    return data_time

async def data_format_x(time):
    time = time.replace(' de ', ' ')
    time = time.replace('.', '')
    time = time.replace(',', '')
    month = data_format_()
    is_j = True
    for i in month:
        if i in time:
            is_j = False
    if is_j:
        for k, v in month.items():
            for i in v:
                if i in time:
                    time = time.replace(i, k)
                    break


    time = time.split(' ')

    try:
        int(time[0])
    except Exception:
        time[0], time[1] = time[1], time[0]
    time = ' '.join(time)

    try:
        time_format = datetime.datetime.strptime(time, '%d %b %Y')
    except Exception:
        time_format = datetime.datetime.strptime(time, '%d %B %Y')
    data_time = datetime.datetime.strftime(time_format, '%Y-%m-%d')
    return data_time



