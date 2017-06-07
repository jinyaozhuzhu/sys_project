# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

"""
矩阵计算的相关函数
"""


def bool_matrix_multiply(_m1, _m2):
    """
    bool逻辑矩阵相乘
    :param _m1: 矩阵1
    :param _m2: 矩阵2
    :return: 计算结果
    """
    _m1 = np.array(_m1)
    _m2 = np.array(_m2)
    size = _m1.shape[1]
    new_m = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            s = 0
            for k in range(size):
                s = s + _m1[i][k] * _m2[k][j]
                s = 1 if s > 0 else 0
            new_m[i][j] = s

    return new_m


def reachable_matrix(_m):
    """
    返回一个邻接矩阵的可达矩阵
    :param _m:  邻接矩阵
    :return: 可达矩阵
    """
    _m = np.array(_m)
    first_m = _m + np.eye(_m.shape[0])  # A+I
    old_m = bool_matrix_multiply(first_m, first_m)
    b = np.all(first_m == old_m)
    while not b:
        new_m = bool_matrix_multiply(old_m, first_m)
        b = np.all(new_m == old_m)
        old_m = new_m
    return old_m


def meduction_matrix(matrix):
    """
    计算可达矩阵的缩减矩阵
    :param matrix: 可达矩阵
    :return: 缩减矩阵
    """
    size = matrix.shape[0]
    number_list = [i for i in range(1, size + 1)]
    ma_df = pd.DataFrame(matrix, index=number_list, columns=number_list)
    ma_df.drop_duplicates(inplace=True)
    ma_df_t = ma_df.T
    ma_df_t.drop_duplicates(inplace=True)
    return ma_df_t.T


def matrix_set(r_m):
    """
    计算可达矩阵的集合
    :param r_m: 可达矩阵
    :return: 各个元素的各种集合，以及矩阵的起始集和终止集
    """
    size = r_m.shape[0]
    total_dict = dict()
    for k1 in range(1, size + 1):  # 初始化字典
        temp = dict()
        for k2 in ['a', 'c', 'r']:
            temp[k2] = {}
        total_dict[k1] = temp
    for i in range(size):  # 计算要素的可达集,先行集，共同集
        r_set = set()
        a_set = set()
        for j in range(size):
            if r_m[i][j] == 1:
                r_set.add(j + 1)
            if r_m[j][i] == 1:
                a_set.add(j + 1)
        total_dict[i + 1]['r'] = r_set
        total_dict[i + 1]['a'] = a_set
        total_dict[i + 1]['c'] = r_set & a_set

    b_set = set()  # 起始集
    e_set = set()  # 终止集
    for k in range(1, size + 1):
        if total_dict[k]['a'] == total_dict[k]['c']:
            b_set.add(k)
        if total_dict[k]['r'] == total_dict[k]['c']:
            e_set.add(k)
    total_dict['b'] = b_set
    total_dict['e'] = e_set
    return total_dict


def begin_reach_set(r_m):
    """
    只获取每个起始集的可达集，并且以字典返回
    :param r_m: 可达矩阵
    :return:
    """
    total_dict = matrix_set(r_m)
    begin_reach = dict()
    begin_set = total_dict['b']
    for i in begin_set:
        begin_reach[i] = total_dict[i]['r']
    return begin_reach


def piece_diagonal(r_m):
    """
    计算可达矩阵的块对角阵
    :param r_m: 可达矩阵
    :return: 块对角阵
    """
    begin_reach = begin_reach_set(r_m)
    size = r_m.shape[0]
    nums = [i for i in range(1, size + 1)]
    df = pd.DataFrame(r_m, index=nums, columns=nums, dtype=int)

    keys = list(begin_reach.keys())
    i = 0
    while i < len(keys) - 1:
        key_i = keys[i]
        value_i = begin_reach[key_i]
        for j in range(i + 1, len(keys)):
            keys_j = keys[j]
            value_j = begin_reach[keys_j]
            # 如果存在不是空集，则合并集合 循环计算之后两两集合之间必定是空集
            if value_i & value_j != set():
                new_value = value_i | value_j
                begin_reach.pop(key_i)
                begin_reach.pop(keys_j)
                begin_reach[keys_j, key_i] = new_value
                keys = list(begin_reach.keys())
                i = 0
                break
            i = i + 1
    result = dict()
    keys = list(begin_reach.keys())
    for k in range(0, len(keys)):
        key_k = keys[k]
        result[k + 1] = df.ix[begin_reach[key_k], begin_reach[key_k]]
    return result
