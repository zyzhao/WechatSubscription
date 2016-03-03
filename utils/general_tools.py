# -*- coding: utf-8 -*-
import date_helper
from random import randint
import uuid
import cPickle
import socket

def create_user_grid_id():
    """
    生产UserGrid ID

    :return:
    """
    current_date = date_helper.now_dt()
    random_num = randint(100000, 999999)    # 随机生成6位
    random_curr = current_date.strftime('%Y%m%d%H%M%S')+str(random_num)

    return random_curr


def make_uuid():
    """
    生成 UUID

    :return:
    """
    uuid_rand = str(uuid.uuid1())+'-'+str(randint(1, 10000))

    return uuid_rand


def get_server_ip():
    """
    获取当前运行机器的IP

    :return:
    """

    server_ip = socket.gethostbyname(socket.gethostname())
    return server_ip


def save_to_pickle(data, file_name):
    """
    保存数据内容去pickle文件

    :param data:
    :param file_name:
    :return:
    """
    with open(file_name, 'wb') as fp:
        cPickle.dump(data, fp)


def read_pickle(file_name):
    """
    read pickle

    :param file_name:
    :return:
    """
    with open(file_name, 'r') as fp:
        data_opt = cPickle.load(fp)

    return data_opt


def write_exception_token_to_csv(tk, file_name):
    with open(file_name, 'a') as fp:
        fp.write(tk+'\n')


def df_to_dict(df):
    """
    把pd.Dataframe 转成 dict

    :param df: Df
    :return:
    """
    out = {}
    for nm in df.columns:
        out[nm] = list(df[nm])
    return out


def df_to_list( df):
    """
    把pd.Dataframe 转成 list

    :param df: Df
    :return:
    """
    out = []
    if not df.empty:
        for idx in df.index:
            obs = df.loc[idx].to_dict()
            out.append(obs)
    return out




