# -*- coding: utf-8 -*-
# Enrico F. D.
# 09/03/2020
# Insper - Camada Física da Computação


import time
from threading import Thread


class Rx(object):
    def __init__(self, physics):
        self.physics = physics
        self.buffer = bytes(bytearray())
        self.thread_stop = False
        self.thread_mutex = True
        self.READLEN = 1024

    def thread(self):
        while not self.thread_stop:
            if self.thread_mutex == True:
                rx_temp, n_rx = self.physics.read(self.READLEN)
                if n_rx > 0:
                    self.buffer += rx_temp
                time.sleep(0.01)

    def thread_start(self):
        self.thread = Thread(target=self.thread, args=())
        self.thread.start()

    def thread_kill(self):
        self.thread_stop = True

    def thread_pause(self):
        self.thread_mutex = False

    def thread_resume(self):
        self.thread_mutex = True

    def get_is_empty(self):
        if self.get_buffer_len() == 0:
            return True
        else:
            return False

    def get_buffer_len(self):
        return len(self.buffer)

    def get_all_buffer(self, len):
        self.thread_pause()
        b = self.buffer[:]
        self.clear_buffer()
        self.thread_resume()
        return b

    def get_buffer(self, limit):
        self.thread_pause()
        b = self.buffer[0:limit]
        time = self.buffer[limit : limit + 17]
        self.buffer = self.buffer[limit:]
        self.thread_resume()
        return b, time

    def get_n_data(self):
        while bytes([255, 255, 255]) not in self.buffer:
            time.sleep(0.05)
        size = self.check_last_value()
        return self.get_buffer(size)

    def clear_buffer(self):
        self.buffer = b""

    def check_last_value(self):

        received = [self.buffer[i : i + 1] for i in range(0, len(self.buffer), 1)]
        index = []

        while b"\xff" in received:
            index.append(received.index(b"\xff"))
            received.remove(b"\xff")

        answer = [x for x in index if index.count(x) > 2]
        rest = len(index) - 3

        return answer[len(answer) - 1] + rest - 17
