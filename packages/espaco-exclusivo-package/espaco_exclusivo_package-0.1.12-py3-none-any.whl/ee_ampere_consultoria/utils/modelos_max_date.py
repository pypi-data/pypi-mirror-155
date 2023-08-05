# -*- coding: utf-8 -*-
"""
    --------------------------------------------------------------------------------------------------------------------

    Description: 
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Obs.: 

    Author:           @diego.yosiura
    Last Update:      01/02/2022 15:50
    Created:          23/07/2021 18:04
    Copyright:        (c) Ampere Consultoria Ltda
    Original Project: espaco-exclusivo-package
    IDE:              PyCharm
"""
from datetime import datetime
from datetime import timedelta

from ..produtos.meteorologia import Modelos
from ..produtos.meteorologia import DiasModelos


def check_global_max_date() -> datetime:
    n_max = 0
    for m in DiasModelos:
        if m.value > n_max:
            n_max = m.value

    now = datetime.utcnow()
    global_max = now + + timedelta(days=n_max)
    return global_max.date()


def check_modelo_max_date(modelo: Modelos) -> datetime:
    m = getattr(DiasModelos, modelo.name)
    if m is None:
        return None

    now = datetime.utcnow()
    model_max = now + timedelta(days=m.value)
    return model_max.date()
