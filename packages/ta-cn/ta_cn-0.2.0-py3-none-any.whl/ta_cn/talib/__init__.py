#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author     :wukan
# @License    :(C) Copyright 2022, wukan
# @Date       :2022-06-16
"""
Examples
--------
只要替换导入即可直接支持二维矩阵
>>> import talib as ta
>>> import ta_cn.talib as ta

"""
import sys as _sys

import numpy as np
import pandas as pd
import talib as _talib
from talib import abstract as _abstract


def tafunc_nditer(tafunc, args, kwargs, output_names):
    """数据应用函数

    Parameters
    ----------
    tafunc
        计算单列的函数
    output_names: list
        tafunc输出参数名

    Returns
    -------
    tuple
        输出数组

    """

    def is_np_pd(x):
        """是否几种特数类型"""
        return isinstance(x, (pd.DataFrame, pd.DataFrame, np.ndarray))

    def pd_to_np(x):
        """pandas格式转numpy"""
        if isinstance(x, (pd.Series, pd.DataFrame)):
            return x.values
        return x

    # 分组
    args_input = [pd_to_np(v) for v in args if is_np_pd(v)]  # 位置非数字参数
    args_param = [pd_to_np(v) for v in args if not is_np_pd(v)]  # 位置数字参数
    kwargs_input = {k: pd_to_np(v) for k, v in kwargs.items() if is_np_pd(v)}  # 命名非数字参数
    kwargs_param = {k: pd_to_np(v) for k, v in kwargs.items() if not is_np_pd(v)}  # 命名数字参数

    # 取一个非数字，得用于得到形状
    if len(args_input) > 0:
        real = args_input[0]
    else:
        real = list(kwargs_input.values())[0]

    if real.ndim == 1:
        # 一维，直接计算并返回
        return tafunc(*args_input, *args_param, **kwargs_input, **kwargs_param)

    # =====以下是二维======

    # 输出缓存
    outputs = [np.empty_like(real) for _ in output_names]
    # 输入源
    inputs = [*args_input, *kwargs_input.values()]

    with np.nditer(inputs + outputs,
                   flags=['external_loop'], order='F',
                   op_flags=[['readonly']] * len(inputs) + [['writeonly']] * len(outputs)) as it:
        for in_out in it:
            _in = in_out[:len(inputs)]  # 分离输入
            args_in = in_out[:len(args_input)]  # 分离位置输入
            kwargs_in = {k: v for k, v in zip(kwargs_input.keys(), _in[len(args_input):])}  # 分离命名输入

            # 计算并封装
            ta_out = tafunc(*args_in, *args_param, **kwargs_in, **kwargs_param)
            if not isinstance(ta_out, tuple):
                ta_out = tuple([ta_out])

            # 转存数据
            _out = in_out[len(inputs):]  # 分离输出
            for _i, _o in zip(_out, ta_out):
                _i[...] = _o

    # 输出
    if len(outputs) == 1:
        return outputs[0]
    return outputs


def _make_func(func, func_name, globals_):
    """复制一个函数，并命名"""
    import types as _types

    code_obj = func.__code__

    attr_list = ['co_argcount',
                 'co_kwonlyargcount',
                 'co_nlocals',
                 'co_stacksize',
                 'co_flags',
                 'co_code',
                 'co_consts',
                 'co_names',
                 'co_varnames',
                 'co_filename',
                 'co_name',
                 'co_firstlineno',
                 'co_lnotab']
    if _sys.version_info >= (3, 8):
        attr_list = ['co_argcount',
                     'co_posonlyargcount',
                     'co_kwonlyargcount',
                     'co_nlocals',
                     'co_stacksize',
                     'co_flags',
                     'co_code',
                     'co_consts',
                     'co_names',
                     'co_varnames',
                     'co_filename',
                     'co_name',
                     'co_firstlineno',
                     'co_lnotab']
    co_kwargs = {k[3:]: getattr(code_obj, k) for k in attr_list}
    co_kwargs['name'] = func_name  # 函数名在这里设置

    mycode_obj = _types.CodeType(*co_kwargs.values())
    return _types.FunctionType(mycode_obj, globals_, func_name, ())


def _ta_func(*args, **kwargs):
    """TA函数转发"""
    # 获取新函数名
    func_name = _sys._getframe().f_code.co_name

    # 获取指标信息
    info = _abstract.Function(func_name)._Function__info

    return tafunc_nditer(getattr(_talib, func_name),
                         args, kwargs,
                         info['output_names'])


for func_name in _talib.get_functions():
    """talib遍历"""
    _func = getattr(_talib, func_name)
    _f = _make_func(_ta_func, func_name, globals())

    _f.__doc__ = _func.__doc__
    globals()[func_name] = _f
