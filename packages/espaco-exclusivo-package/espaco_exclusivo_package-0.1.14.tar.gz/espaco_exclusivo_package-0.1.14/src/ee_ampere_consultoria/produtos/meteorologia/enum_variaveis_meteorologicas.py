# -*- coding: utf-8 -*-
"""
    --------------------------------------------------------------------------------------------------------------------

    Description: 
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Obs.: 

    Author:           @diego.yosiura
    Last Update:      21/07/2021 19:49
    Created:          21/07/2021 19:49
    Copyright:        (c) Ampere Consultoria Ltda
    Original Project: espaco_exclusivo_package
    IDE:              PyCharm
"""
from enum import Enum


class VariaveisMeteorologicas(Enum):
    HGT = 'hgt'
    TMP = 'tmp'
    TMAX = 'tmax'
    TMIN = 'tmin'
    PREC = 'prec'
    RH = 'rh'
    UWIND = 'uwind'
    VWIND = 'vwind'
    PRESSUP = 'pressup'
    TCC = 'tcc'
    DSWRF = 'dswrf'
