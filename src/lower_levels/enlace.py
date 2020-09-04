# -*- coding: utf-8 -*-
# Enrico F. D.
# 09/03/2020
# Insper - Camada Física da Computação

import time

from src.lower_levels.physical_interface import Physics
from src.lower_levels.enlace_rx import Rx
from src.lower_levels.enlace_tx import Tx


class Enlace(object):
    def __init__(self, name):
        self.physics = Physics(name)
        self.rx = Rx(self.physics)
        self.tx = Tx(self.physics)
        self.connected = False

    def enable(self):
        self.physics.open()
        self.rx.thread_start()
        self.tx.thread_start()

    def disable(self):
        self.rx.thread_kill()
        self.tx.thread_kill()
        time.sleep(1)
        self.physics.close()

    def send_data(self, data):
        self.tx.send_buffer(data)

    def get_data(self):
        data, time = self.rx.get_n_data()
        return (data, time)
