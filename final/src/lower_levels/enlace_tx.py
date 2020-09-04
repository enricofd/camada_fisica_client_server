# -*- coding: utf-8 -*-
# Enrico F. D.
# 09/03/2020
# Insper - Camada Física da Computação

import time
from threading import Thread


class Tx(object):
    def __init__(self, physics):
        self.physics = physics
        self.buffer = bytes(bytearray())
        self.trans_len = 0
        self.empty = True
        self.thread_mutex = False
        self.thread_stop = False

    def thread(self):
        while not self.thread_stop:
            if self.thread_mutex:
                self.trans_len = self.physics.write(self.buffer)
                self.thread_mutex = False

    def thread_start(self):
        self.thread = Thread(target=self.thread, args=())
        self.thread.start()

    def thread_kill(self):
        self.thread_stop = True

    def thread_pause(self):
        self.thread_mutex = False

    def thread_resume(self):
        self.thread_mutex = True

    def send_buffer(self, data):
        self.trans_len = 0
        self.buffer = data
        self.thread_mutex = True

    def get_buffer_len(self):
        return len(self.buffer)

    def get_status(self):
        return self.trans_len

    def get_is_bussy(self):
        return self.thread_mutex

