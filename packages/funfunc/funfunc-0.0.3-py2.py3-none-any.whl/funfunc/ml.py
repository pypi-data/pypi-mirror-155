# -*- coding: utf-8 -*-
# AUTHOR  : wjia
# TIME    : 2022/6/21 17:14
# FILE    : ml
# PROJECT : funfunc
# IDE     : PyCharm

def pandas_max_print() -> None:
    import pandas as pd

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
