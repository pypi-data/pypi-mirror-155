# -*- coding: utf-8 -*-
# 成交量型指标

from .arithmetic import *


@arithmetic_wrapper
def OBV(M=30):
    """累计能量线

    公式：
        VA:=IF(CLOSE>REF(CLOSE,1),VOL,-VOL);
        OBV:SUM(IF(CLOSE=REF(CLOSE,1),0,VA),0);
        MAOBV:MA(OBV,M);
    输入：
        M: 统计的周期数 M
    输出：
        OBV: OBJ值
        MAOBV: OBJ的M周期移动平均
    定义：
        RETURNS=(OBV, MAOBV)

    """

    VA = IF(CLOSE>REF(CLOSE, 1), VOL, -VOL)
    OBV = SUM(IF(CLOSE==REF(CLOSE, 1), 0, VA), 0)
    MAOBV = MA(OBV, M)

    return OBV, MAOBV
