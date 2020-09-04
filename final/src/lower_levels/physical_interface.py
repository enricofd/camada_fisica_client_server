#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#####################################################
#Carareto
#17/02/2018
####################################################

# Importa pacote de comunicação serial
import serial

# importa pacote para conversão binário ascii
import binascii

#################################
# Interface com a camada física #
#################################
class Physics(object):
    def __init__(self, name):
        self.name        = name
        self.port        = None
        #self.baudrate    = 115200
        self.baudrate    = 9600
        self.bytesize    = serial.EIGHTBITS
        self.parity      = serial.PARITY_NONE
        self.stop        = serial.STOPBITS_ONE
        self.timeout     = 0.1
        self.rx_remain    = b""

    def open(self):
        self.port = serial.Serial(self.name,
                                  self.baudrate,
                                  self.bytesize,
                                  self.parity,
                                  self.stop,
                                  self.timeout)


    def close(self):
        self.port.close()

    def flush(self):
        self.port.flushInput()
        self.port.flushOutput()

    def encode(self, data):
        encoded = binascii.hexlify(data)
        return(encoded)

    def decode(self, data):
        """ RX ASCII data after reception
        """
        decoded = binascii.unhexlify(data)
        return(decoded)

    def write(self, tx_buffer):
        """ Write data to serial port

        This command takes a buffer and format
        it before transmit. This is necessary
        because the pyserial and arduino uses
        Software flow control between both
        sides of communication.
        """
        n_tx = self.port.write(self.encode(tx_buffer))
        self.port.flush()
        return(n_tx/2)

    def read(self, n_bytes):
        """ Read nBytes from the UART com port

        Nem toda a leitura retorna múltiplo de 2
        devemos verificar isso para evitar que a funcao
        self.decode seja chamada com números ímpares.
        """
        rx_buffer = self.port.read(n_bytes)
        rx_buffer_concat = self.rx_remain + rx_buffer
        n_valid = (len(rx_buffer_concat)//2)*2
        rx_buffer_valid = rx_buffer_concat[0:n_valid]
        self.rx_remain = rx_buffer_concat[n_valid:]
        try :
            """ As vezes acontece erros na decodificacao
            fora do ambiente linux, isso tenta corrigir
            em parte esses erros. Melhorar futuramente."""
            "muitas vezes um flush no inicio resolve!"
            rx_buffer_decoded = self.decode(rx_buffer_valid)
            n_rx = len(rx_buffer)
            return(rx_buffer_decoded, n_rx)
        except :
            print("[ERRO] interfaceFisica, read, decode. buffer : {}".format(rx_buffer_valid))
            return(b"", 0)

