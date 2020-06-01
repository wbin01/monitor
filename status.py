#!/usr/bin/env python3
import random


class StatusEmulator(object):
    history = dict()

    def __init__(self, min_value=0, max_value=10):
        self.min = min_value
        self.max = max_value

        self._set_history()

    def _get_history(self):
        if id(self) not in self.history:
            history = {"min": self.min, "max": self.max, "current": 0, "inverse": False}

        else:
            history = self.history[id(self)]

        return history

    def _set_history(self):
        self.history[id(self)] = self._get_history()

    def get_value(self):
        history = self._get_history()
        # Valor inicial do monitoramento
        v = history["current"]
        # Valor máximo do monitoramento
        max_v = history["max"]
        # Valor mínimo do monitoramento
        min_v = history["min"]
        # Flag para inverter números aleatórios
        inverse = history["inverse"]

        if inverse:
            v -= random.randrange(0, 2)
        else:
            v += random.randrange(0, 2)

        # Se valor chegar ao número máximo de linhas, inverte ordem para decrementar
        if v >= max_v:
            history["inverse"] = True
            v = random.randrange(round(v / 2), max_v)  # Não deixa passar do máximo

        # Se chegar a 0, inverte ordem para incrementar
        elif v <= min_v:
            history["inverse"] = False
            v = random.randrange(min_v, round(max_v / 2))  # Não deixa ser menor que o mínimo

        history["current"] = v
        self.history[id(self)] = history

        return v
