# -*- coding: utf-8 -*-
"""
    --------------------------------------------------------------------------------------------------------------------

    Description: 
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Obs.: 

    Author:           @diego.yosiura
    Last Update:      01/02/2022 15:50
    Created:          23/07/2021 16:57
    Copyright:        (c) Ampere Consultoria Ltda
    Original Project: espaco-exclusivo-package
    IDE:              PyCharm
"""
import re
from datetime import datetime
from datetime import timedelta

from ... import Configuration
from ...utils import check_global_max_date

from ..meteorologia import Modelos

from . import BodyFluxPersonalizadoCenario
from . import BodyFluxPersonalizadoCenarioBloco


class BodyFluxPersonalizado:
    __ds_nome_estudo = None
    __ds_nome_cenario = None
    __dt_inicio = None
    __dt_fim = None
    __cenarios = None

    def set_nome_estudo(self, nome: str):
        self.__ds_nome_estudo = re.sub(r'[^A-z0-9_-]', '', str(nome).upper())
        if len(self.__ds_nome_estudo) <= 3:
            raise Exception("[EE BodyFluxPersonalizado] - O nome do estudo deve conter "
                            "mais de 3 caracteres válidos. [{}]".format(self.__ds_nome_estudo))
        self.__ds_nome_cenario = self.__ds_nome_estudo

        if self.__cenarios is not None:
            self.__cenarios[0].ds_nome = self.__ds_nome_cenario

    def set_periodo_analise(self, inicio: datetime, fim: datetime):
        inicio = datetime(inicio.year, inicio.month, inicio.day).date()
        fim = datetime(fim.year, fim.month, fim.day).date()

        if fim > check_global_max_date():
            raise Exception("[EE BodyFluxPersonalizado] - O fim do estudo {} excede o "
                            "período máximo de estudo {}.".format(fim, check_global_max_date()))

        now = datetime.utcnow() - timedelta(hours=3)
        today = now.date()
        tomorrow = today + timedelta(days=1)

        if not inicio == tomorrow:
            raise Exception("[EE BodyFluxPersonalizado] - O inicio do estudo deve ser a data de amanha (D+1).")
        if fim <= inicio:
            raise Exception("[EE BodyFluxPersonalizado] - O fim do estudo deve ser maior que a data de inicio.")
        self.__dt_inicio = inicio
        self.__dt_fim = fim

    def add_bloco(self, ds_modelo: Modelos, ck_rmv: bool, dt_data_prev: datetime,
                  dt_inicio: datetime, dt_fim: datetime):
        try:
            dt_data_prev = datetime(dt_data_prev.year, dt_data_prev.month, dt_data_prev.day).date()
            dt_inicio = datetime(dt_inicio.year, dt_inicio.month, dt_inicio.day).date()
            dt_fim = datetime(dt_fim.year, dt_fim.month, dt_fim.day).date()

            if self.__cenarios is None:
                self.__cenarios = []
            if len(self.__cenarios) <= 0:
                self.__cenarios.append(BodyFluxPersonalizadoCenario())
                self.__cenarios[0].ds_nome = self.__ds_nome_cenario

            self.__cenarios[0].add_bloco(ds_modelo, dt_data_prev, ck_rmv, dt_inicio, dt_fim)
        except Exception as e:
            error = "[EE BodyFluxPersonalizado] - Erro não tratado: {}".format(str(e))
            Configuration.debug_print(error, e)
            raise Exception(error)

    def get_json(self):
        datetime_inicio = datetime(self.__dt_inicio.year, self.__dt_inicio.month, self.__dt_inicio.day, 12)
        datetime_fim = datetime(self.__dt_fim.year, self.__dt_fim.month, self.__dt_fim.day, 12)
        json_response = {
            'ds_nome_estudo': self.__ds_nome_estudo,
            'ds_nome_cenario': self.__ds_nome_cenario,
            'dt_inicio': datetime_inicio.timestamp(),
            'dt_fim': datetime_fim.timestamp(),
            'cenarios': [],
        }

        for c in self.__cenarios:
            c.validate()
            blocos = []
            if c.blocos[0].dt_inicio != self.__dt_inicio or c.blocos[-1].dt_fim != self.__dt_fim:
                raise Exception("Os blocos de cada cenário devem compreender todo o período de estudo. "
                                "{} - {} | Inicio Bloco 01 [{}] | Fim Bloco n [{}]".format(self.__dt_inicio,
                                                                                           self.__dt_fim,
                                                                                           c.blocos[0].dt_inicio,
                                                                                           c.blocos[-1].dt_fim))
            for b in c.blocos:
                datetime_dataprev = datetime(b.dt_data_prev.year, b.dt_data_prev.month, b.dt_data_prev.day,12)
                datetime_binicio = datetime(b.dt_inicio.year, b.dt_inicio.month, b.dt_inicio.day,12)
                datetime_bfim = datetime(b.dt_fim.year, b.dt_fim.month, b.dt_fim.day,12)

                blocos.append({
                    "ds_modelo": b.ds_modelo.value,
                    "dt_data_prev": datetime_dataprev.timestamp(),
                    "ck_rmv": b.ck_rmv,
                    "dt_inicio": datetime_binicio.timestamp(),
                    "dt_fim": datetime_bfim.timestamp()
                })

            json_response['cenarios'].append({'ds_nome': c.ds_nome, 'blocos': blocos})
        return json_response
