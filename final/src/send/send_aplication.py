# -*- coding: utf-8 -*-
# Enrico F. D.
# 09/03/2020
# Insper - Camada Física da Computação

from src.lower_levels.enlace import *
from src.count_time.count_time import time_to_bytes

serial_name = "COM6"  # serial port


def send():
    """
    Function that send the data via serial port
    """
    try:

        com = Enlace(serial_name)  # initialize type Enlace

        # starts com's threads, serial ports
        com.enable()
        
        print("-------------------------")
        print("-------------------------\n")
        path = input("Enter file's path: ")
        
        # get the message
        message = open(path, "rb").read()

        # start cronometer
        time = time_to_bytes()

        # add to the message 3 bytes, which are responsible for alerting the receive apllication where to stop
        tx_buffer = message + time + bytes([255, 255, 255])
        # send the data to serial port
        com.send_data(tx_buffer)

        print("\nMessage sent")
        print("Port: " + serial_name)
        print("Size: " + str(len(tx_buffer)-20) + " bytes")
        print("-------------------------")
        print("-------------------------\n")
        com.disable()

    except:
        print("Message not sent, please try again")
        print("-------------------------")
        print("-------------------------")
        com.disable()

