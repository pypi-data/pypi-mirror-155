# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
@Author  : jingle1267
@Time    : 2019-07-14 20:26
@desc：  : cache, use json to store cache
"""
import hashlib
import json
import os
import threading
import demjson

from LogColorHelper import LogColorHelper

# from src.util import TimeHelper

import sys
sys.setrecursionlimit(100000)

# 缓存绝对路径
CACHE_DIR = '../'

# TODO 添加内存缓存使用，暂未用到
CACHE_FILE_NAMES_VALUES = {}

# 缓存被分割为子缓存文件的文件个数，对数据量较大的情况下帮助明显，类似数据库的分库分表
CACHE_FILE_SECTION_COUNT = 50

R = threading.Lock()


def persist_to_file(file_name):
    def decorator(original_func):

        try:
            cache = json.load(open(os.path.join(CACHE_DIR, file_name), 'r'))
        except (IOError, ValueError):
            cache = {}

        def new_func(param):
            if param not in cache:
                cache[param] = original_func(param)
                json.dump(cache, open(os.path.join(
                    CACHE_DIR, file_name), 'w'), indent=4)
            return cache[param]

        return new_func

    return decorator


# 写缓存，主要校验是否存在
def set_cache(file_name, cache_key, folder_name=''):
    if file_name is None or file_name == '':
        LogColorHelper.red('set_cache 缓存file_name为空')
        return
    if cache_key is None or cache_key == '':
        LogColorHelper.red('set_cache 缓存cacke_key为空')
        return

    file_name = file_name.replace('/', '--')
    if folder_name != '':
        file_path = os.path.join(CACHE_DIR, folder_name, file_name)
    else:
        file_path = os.path.join(CACHE_DIR, file_name)

    # 如果存在缓存文件，则需要做缓存文件转换
    is_old_cache_file_exist = os.path.exists(file_path)
    # print('is_old_cache_file_exist:', is_old_cache_file_exist)
    if is_old_cache_file_exist:
        kv = get_all_kv(file_name, folder_name)
        print('kv.len()', len(kv), file_path)
        # 添加当前要处理的数据
        kv[cache_key] = 1
        # 删除原来的缓存文件
        os.remove(file_path)
        # print(os.remove(file_path))
        for k in kv.keys():
            v = kv[k]
            # TimeHelper.time_counter(
            #     set_cache, file_name=file_name, cache_key=k, folder_name=folder_name)
            set_cache(file_name, k, folder_name)
        return

    sub_folder_name = file_name.replace('.json', '')
    real_cache_file_name = get_sub_cache_file_name(file_name, cache_key)
    if folder_name != '':
        real_file_path = os.path.join(
            CACHE_DIR, folder_name, sub_folder_name, real_cache_file_name)
    else:
        real_file_path = os.path.join(
            CACHE_DIR, sub_folder_name, real_cache_file_name)
    sub_folder_path = real_file_path.replace(real_cache_file_name, '')

    # 如果不存在子目录，则创建子目录
    if not os.path.exists(sub_folder_path):
        os.makedirs(sub_folder_path)

    try:
        R.acquire()
        with open(real_file_path, 'r') as file:
            cache = json.load(file)
    except (IOError, ValueError):
        cache = {}
    finally:
        R.release()

    if cache_key not in cache:
        cache[cache_key] = 1
        try:
            R.acquire()
            with open(real_file_path, 'w') as file:
                json.dump(cache, file, indent=4)
        finally:
            R.release()


# 获取缓存，主要校验是否存在
def get_cache(file_name, cache_key, folder_name=''):
    if file_name is None or file_name == '':
        LogColorHelper.red('get_cache 缓存file_name为空')
        return
    if cache_key is None or cache_key == '':
        LogColorHelper.red('get_cache 缓存cacke_key为空')
        return

    file_name = file_name.replace('/', '--')
    # if folder_name != '':
    #     file_path = os.path.join(CACHE_DIR, folder_name, file_name)
    # else:
    #     file_path = os.path.join(CACHE_DIR, file_name)

    sub_folder_name = file_name.replace('.json', '')
    real_cache_file_name = get_sub_cache_file_name(file_name, cache_key)
    if folder_name != '':
        real_file_path = os.path.join(
            CACHE_DIR, folder_name, sub_folder_name, real_cache_file_name)
    else:
        real_file_path = os.path.join(
            CACHE_DIR, sub_folder_name, real_cache_file_name)

    sub_folder_path = real_file_path.replace(real_cache_file_name, '')

    # 如果不存在子目录，则创建子目录
    if not os.path.exists(sub_folder_path):
        os.makedirs(sub_folder_path)

    try:
        R.acquire()
        with open(real_file_path, 'r') as file:
            cache = json.load(file)
    except (IOError, ValueError):
        print('缓存文件{0}暂不存在'.format(real_file_path))
        cache = {}
    finally:
        R.release()

    if cache_key not in cache:
        # cache[cache_key] = 1
        # json.dump(cache, open(file_name, 'w'), indent=4)
        return 0
    else:
        return 1


# 删除缓存文件，主要校验是否存在
def del_cache_file(file_name):
    try:
        file_name = file_name.replace('/', '--')
        os.remove(os.path.join(CACHE_DIR, file_name))
    except (IOError, ValueError):
        print('删除缓存文件失败')


def get_all_kv(file_name='', folder_name=''):
    try:
        with open(os.path.join(CACHE_DIR, folder_name, file_name), 'r') as f:
            f_str = f.read()
            # print('f_str:', f_str)
            cache = demjson.decode(f_str)
    except (IOError, ValueError) as e:
        LogColorHelper.red('json load error:{0}'.format(e.args))
        cache = {}
    return cache


def get_all_keys(file_name, folder_name=''):
    cache_keys = []
    if os.path.exists(os.path.join(CACHE_DIR, folder_name, file_name)):
        try:
            with open(os.path.join(CACHE_DIR, folder_name, file_name), 'r') as f:
                # lines = f.readlines()
                # for l in lines:
                #     if ':' in l:
                #         chart_str_arr = l.split(':')
                #         chart_id = chart_str_arr[0]
                #         chart_id = chart_id.replace('"', '')
                #         chart_id = chart_id.strip()
                #         cache_keys.append(chart_id)
                content_str = f.read()
                content_json = json.loads(content_str)
                content_keys = content_json.keys()
                for k in content_keys:
                    cache_keys.append(k)
        except (IOError, ValueError) as e:
            LogColorHelper.red('json load error:{0}'.format(e.args))
        return cache_keys
    else:
        sub_folder_name = file_name.replace('.json', '')
        sub_folder_path = os.path.join(CACHE_DIR, folder_name, sub_folder_name)
        for i in range(CACHE_FILE_SECTION_COUNT):
            sub_file_name = '{0}_{1}.json'.format(sub_folder_name, i)
            ks = get_all_keys(sub_file_name, os.path.join(
                folder_name, sub_folder_name))
            for k in ks:
                cache_keys.append(k)
            # break
        return cache_keys


# 获取缓存
def get_cache_value(file_name, cache_key):
    try:
        with open(os.path.join(CACHE_DIR, file_name), 'r') as f:
            # file_name = file_name.replace('/', '--')
            # print("==" + open(file_name, 'r').read())
            cache = json.load(f)
    except (IOError, ValueError):
        print('json load error')
        cache = {}

    # print(cache)

    if cache_key not in cache:
        return ''
    else:
        return cache[cache_key]


# 设置缓存
def set_cache_value(file_name, cache_key, cache_value):
    try:
        cache = json.load(open(os.path.join(CACHE_DIR, file_name), 'r'))
    except (IOError, ValueError):
        cache = {}

    if cache_key not in cache:
        cache[cache_key] = cache_value
        json.dump(cache, open(os.path.join(
            CACHE_DIR, file_name), 'w'), indent=4)
    else:
        cache[cache_key] = cache_value
        json.dump(cache, open(os.path.join(
            CACHE_DIR, file_name), 'w'), indent=4)


# 删除缓存文件
def del_cache_value_file(file_name):
    try:
        os.remove(os.path.join(CACHE_DIR, file_name))
    except (IOError, ValueError):
        print('删除缓存文件失败')


def easy_cache2(folder_name, file_name, cache_key, hit_callback, miss_callback, **kwargs):
    cache_value = get_cache(file_name, cache_key, folder_name)
    if cache_value == 1:
        if hit_callback is not None:
            hit_callback(**kwargs)
        return 1
    else:
        if miss_callback(**kwargs):
            set_cache(file_name, cache_key, folder_name)


# 缓存是否存在便利工具
# file_name: 缓存文件名称
# cache_key：缓存字段名
# hit_callback：命中缓存需要执行的回调
# miss_callback：没有命中缓存需要执行的回调
# kwargs：回调需要传的参数
def easy_cache(file_name, cache_key, hit_callback, miss_callback, **kwargs):
    cache_value = get_cache(file_name, cache_key)
    if cache_value == 1:
        if hit_callback is not None:
            hit_callback(**kwargs)
    else:
        if miss_callback is None:
            return
        if miss_callback(**kwargs):
            set_cache(file_name, cache_key)


def get_sub_cache_file_name(file_name='', cache_key=''):
    hash_key = get_hash_key(cache_key)
    sub_folder_name = file_name.replace('.json', '')
    real_cache_file_name = '{0}_{1}.json'.format(sub_folder_name, hash_key)
    return real_cache_file_name


def get_hash_key(key_str):
    return hash(key_str) % CACHE_FILE_SECTION_COUNT


def hash(param_str=''):
    hash_str = hashlib.md5(param_str.encode('utf-8')).hexdigest()
    return int('0x{0}'.format(hash_str[-2:]), 16)


if __name__ == '__main__':
    print('test FileCache.py')

    # file_name = 'wps_change_theme.json'
    # print(len(get_all_keys(file_name)))
    # set_cache(file_name, 'https://aippt.wps.cn/edit/5895055')
    # print(len(get_all_keys(file_name)))
    print()
