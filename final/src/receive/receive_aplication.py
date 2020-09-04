# -*- coding: utf-8 -*-
# Enrico F. D.
# 09/03/2020
# Insper - Camada Física da Computação

from src.lower_levels.enlace import *
import time

serial_name = "COM7"


def receive():
    try:

        com = Enlace(serial_name)

        com.enable()

        rx_buffer, time_sent = com.get_data()

        time_sent_main_raw = [
            str(int.from_bytes([x], byteorder="big")) for x in time_sent[0:10]
        ]
        time_sent_mili_raw = [
            str(int.from_bytes([x], byteorder="big")) for x in time_sent[10::]
        ]

        separator = ""
        time_sent = float(
            separator.join(time_sent_main_raw)
            + "."
            + separator.join(time_sent_mili_raw)
        )

        total_time = round(time.time() - time_sent, 3)

        print("\n-------------------------")
        print("-------------------------\n")

        path = input("Enter path for saving file: ")
        f = open(path, "wb")
        f.write(rx_buffer)
        f.close()

        print("\nReceived")
        print("Port: " + serial_name)
        print("Payload size: " + str(len(rx_buffer)) + " bytes")
        print("Total elapsed time: " + str(total_time) + " seconds")
        print(
            "Total transfer speed: "
            + str(round((len(rx_buffer) + 20) / total_time, 3))
            + " bytes/seconds"
        )
        print("End of communication")
        print("-------------------------")
        print("-------------------------")
        com.disable()
    
    except:
        print("Message not received, please try again")
        print("-------------------------")
        print("-------------------------")
        com.disable()

