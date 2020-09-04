# -*- coding: utf-8 -*-
# Enrico F. D.
# 09/03/2020
# Insper - Camada Física da Computação

from threading import Thread

from src.receive.receive_aplication import receive
from src.send.send_aplication import send


def main():
    """run both, send and receive, at the same time"""

    Thread(target=send).start()
    Thread(target=receive).start()


if __name__ == "__main__":
    main()
