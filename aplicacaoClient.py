
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Fisica da Computacao
#Carareto
#17/02/2018

####################################################



def int_to_byte(values, length):
    result = []
    for i in range(0,length):
        result.append(values >> (i*8)& 0xff)

    result.reverse()

    return result

def sistemaEnvio(payload, com):
    com.enable()
    print("porta COM aberta com sucesso")


    #Variaveis
    timerparaACKNACK = 20
    enviou01 = False
    chegouresposta2 = False
    enviouresposta3 = False
    envioupayload = False
    chegoupayloadnoserver = False
    chegoupayloadcerto = False
    temtimout = False

    com.sendData(None,1)
    enviou01 = True
    esperaresposta2 = True
    temtimout = True


    while True:
        bufferLen = com.rx.getBufferLen(temtimout)
        print("bufferLen: ",bufferLen)
        messaType = -1
        if bufferLen == 0:
            print("Não entrou nada")
        else:
            resultData, resultDataLen, messaType ,ack= com.getData(bufferLen)

        if messaType == 1:
            print("Erro")
        elif messaType == 2 and enviou01:
            chegouresposta2 = True
            print("Servidor ouvindo corretamente")
            com.sendData(None, 3)
            enviouresposta3 = True
            print("\nAvisando o server que estou ouvindo")
            time.sleep(5)
            com.sendData(payload,4)
            print("\nEnviando payload")
            envioupayload = True
            temtimout = False


        elif messaType == 5:
            print("Servidor recebeu corretamente os dados do Payload")
            chegoupayloadnoserver = True
            chegoupayloadcerto = True


        elif messaType == 6:
            chegoupayloadnoserver = True
            chegoupayloadcerto = False
            print("Servidor recebeu os dados mas pacote estava corrompido")
            #Reenviando payload
            print("\nReenviando dados")
            com.sendData(payload,4)
            timerparaACKNACK = 20

        elif messaType == 7:
            com.disable()
            print("Fechando Comunicação\n\n\n")
            time.sleep(1)
            print("-------------------------")
            print("Comunicacao encerrada")
            print("-------------------------")
            break


        elif enviou01 and not chegouresposta2 and bufferLen == 0:
            print("Erro 1: Não recebimento da mensagem 2")
            time.sleep(1)
            print("\nReenviando mensagem 1")
            enviou01 = True
            com.sendData(None, 1)

        elif bufferLen == 0 and envioupayload:
            time.sleep(1)
            timerparaACKNACK-=1
            if timerparaACKNACK == 0:
                print("Erro 3: Não recebimento de mensagem ACK/NACK")












print("comecou")

from enlace import *
import time
from PIL import Image,ImageDraw
import io,os
import tkinter as tk
import tkinter.filedialog as fdlg


# voce devera descomentar e configurar a porta com atraves da qual ira fazer a
# comunicacao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/cu.usbmodem1421" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)






def main():

    nasme = fdlg.askopenfilename()
    img = Image.open(nasme, mode='r')

    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='JPEG')
    imgByteArr = imgByteArr.getvalue()
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)

    # Ativa comunicacao
    sistemaEnvio(imgByteArr, com)
    #verificar que a comunicacao foi aberta


    # Atualiza dados da transmissao
    #txSize = com.tx.getStatus()




    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
