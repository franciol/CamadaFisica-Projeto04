#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Construct Struct
#from construct import *

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX
import facadeEnlace

class enlace(object):
    """ This class implements methods to the interface between Enlace and Application
    """

    def __init__(self, name):
        """ Initializes the enlace class
        """
        self.fisica      = fisica(name)
        self.rx          = RX(self.fisica)
        self.tx          = TX(self.fisica)
        self.connected   = False

    def enable(self):
        """ Enable reception and transmission
        """
        self.fisica.open()
        self.rx.threadStart()
        self.tx.threadStart()

    def disable(self):
        """ Disable reception and transmission
        """
        self.rx.threadKill()
        self.tx.threadKill()
        time.sleep(1)
        self.fisica.close()

    ################################
    # Application  interface       #
    ################################
    def sendData(self, data, messageType):
        """ Send data over the enlace interface
        """
        dataEncap = facadeEnlace.encapsulate(data, messageType)
        self.tx.sendBuffer(dataEncap)

    def getData(self, size):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        print('entrou na leitura e tentara ler ' + str(size) )
        data = self.rx.getNData(size)
        resultData,txLen, messageType, ack = facadeEnlace.readHeadNAll(bytearray(data))

        return(resultData, len(resultData), messageType, ack)
