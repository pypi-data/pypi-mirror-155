#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/20 11:43
# @Author  : lj
# @File    : url_parse.py


def urlparse(url_string:str):
    '''url解析'''
    data = {
        'scheme':'',
        'netloc':'',
        'path':[],
        'query':{}
    }

    if url_string.startswith('https://'):
        data['scheme'] = 'https'
        url_string = url_string.replace('https://','')

    elif url_string.startswith('http://'):
        data['scheme'] = 'http'
        url_string = url_string.replace('http://', '')


    url_is_split_ = url_string.split('?',1)
    url_is_split_path = url_is_split_[0].split('/')

    data['netloc'] = url_is_split_path[0]

    for i in url_is_split_path[1:]:
        data['path'].append(i)

    query_path_list = url_is_split_[-1].split('?')

    query_list = query_path_list[-1].split('&')

    for i in query_list:
        v = i.split('=')
        data['query'][v[0]] = v[-1]

    return data

async def urlparse_x(url_string:str):
    '''url解析'''
    data = {
        'scheme':'',
        'netloc':'',
        'path':[],
        'query':{}
    }

    if url_string.startswith('https://'):
        data['scheme'] = 'https'
        url_string = url_string.replace('https://','')

    elif url_string.startswith('http://'):
        data['scheme'] = 'http'
        url_string = url_string.replace('http://', '')

    url_is_split_ = url_string.split('?', 1)
    url_is_split_path = url_is_split_[0].split('/')

    data['netloc'] = url_is_split_path[0]

    for i in url_is_split_path[1:]:
        data['path'].append(i)

    query_path_list = url_is_split_[-1].split('?')

    query_list = query_path_list[-1].split('&')

    for i in query_list:
        v = i.split('=')
        data['query'][v[0]] = v[-1]

    return data


if __name__ == '__main__':
    url_string = 'https://www.amazon.es/product-reviews/B095NLTZNF/ref=cm_cr_getr_d_paging_btm_next_1?ie=UTF8&sortBy=recent&pageNumber=1&formatType=current_format'
    print(urlparse(url_string))