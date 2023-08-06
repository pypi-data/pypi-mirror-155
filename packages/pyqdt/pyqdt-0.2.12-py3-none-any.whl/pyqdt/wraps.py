# -*- coding: utf-8 -*-

import pandas
from inspect import isfunction


class JQWraps:
    def __init__(self, module):
        for v in dir(module):
            f = getattr(module, v)
            if isfunction(f):
                f = self._wraps(f)
            setattr(self, v, f)

    @classmethod
    def convert_code(cls, data, reverse=False):
        exch_maps = {'SH': 'XSHG', 'SZ': 'XSHE'}
        cols_all = ['code', 'sec_code']
        result = data
        if reverse:
            rev = {v: k for k, v in exch_maps.items()}
            exch_maps = rev
        if type(data) == str:
            arr = data.split('.')
            if len(arr) == 2 and arr[-1] in exch_maps:
                result = arr[0] + '.' + exch_maps[arr[-1]]
        elif type(data) == list:
            result = data.copy()
            for i in range(len(result)):
                result[i] = cls.convert_code(result[i], reverse=reverse)
        elif type(data) == pandas.Index:
            result = data.copy()
            result = pandas.Index(cls.convert_code(list(result), reverse=reverse))
        elif type(data) == pandas.Series:
            result = data.copy()
            result = pandas.Series(cls.convert_code(list(result), reverse=reverse))
        elif type(data) == pandas.DataFrame:
            result = data.copy()
            converted = False
            # convert columns name
            if not converted:
                rename_maps = dict()
                for i in range(len(result.columns)):
                    c_src = str(result.columns[i])
                    c_dst = cls.convert_code(c_src, reverse=reverse)
                    if c_dst != c_src:
                        rename_maps[c_src] = c_dst
                if rename_maps:
                    result.rename(columns=rename_maps, inplace=True)
                    converted = True
            # convert cells by columns
            if not converted:
                cols_convert = [x for x in result.columns if x in cols_all]
                for c in cols_convert:
                    result[c] = result[c].apply(lambda x: cls.convert_code(str(x), reverse=reverse))
                if cols_convert:
                    converted = True
            # convert cells by index
            if not converted and result.index.dtype == object and len(result) > 0:
                c_src = str(result.index[0])
                c_dst = cls.convert_code(c_src, reverse=reverse)
                if c_src != c_dst:
                    result.index = cls.convert_code(result.index, reverse=reverse)
                    converted = True
        return result

    @classmethod
    def _wraps(cls, func):
        def _wrapper(*args, **kwargs):
            args = list(args)
            for i in range(len(args)):
                args[i] = cls.convert_code(args[i])
            for k, v in kwargs.items():
                if k in ['security', 'security_list', 'index_symbol']:
                    kwargs[k] = cls.convert_code(v)
            result = func(*args, **kwargs)
            result = cls.convert_code(result, True)
            return result

        return _wrapper
