from PIL import Image,ImageDraw
import io,os

EOP = b'/00/00/00/00'
stuffingByte = b'/7a/'



def int_to_byte(values, length):
    result = []
    for i in range(0,length):
        result.append(values >> (i*8)& 0xff)

    result.reverse()

    return bytes(result)

def fromByteToInt(bytes):
    result=0

    for b in bytes:
        result=result*256+int(b)

    return result


def encapsulate(payload, messageType):



    txLen = len(payload)
    print('txLen: 'txLen)
    '''
        Head = 10 bytes:
            payloadLen = 5 bytes
            EOP = 13 bytes
            stuffing = 3 bytes
    '''
    payloadfinal = bytes()
    for i in range(0, len(payload)):
        if EOP == payload[i:i+13]:
            payloadfinal+=stuffingByte
            payloadfinal+=payload[i:i+1]
        else:
            payloadfinal+=payload[i:i+1]

    payloadLen = int_to_byte(txLen,5)
    
    if messageType == 1:
        head = int_to_byte(1,1)+payloadLen+EOP+stuffingByte
        #Cliente manda pedido de comunicação para servidor
    
    elif messageType == 2:
        head = int_to_byte(2,1)+payloadLen+EOP+stuffingByte
        #Servidor responde cliente dizendo que recebeu mensagem tipo 1

    elif messageType == 3:
        head = int_to_byte(3,1)+payloadLen+EOP+stuffingByte    
        #Cliente responde servidor dizendo que recebeu mensagem tipo 2
        #e servidor sabe que a próxima mensagem é tipo 4

    elif messageType == 4:
        head = int_to_byte(4,1)+payloadLen+EOP+stuffingByte
        #Cliente faz efetivamente transmissão para servidor

    elif messageType == 5:
        head = int_to_byte(5,1)+payloadLen+EOP+stuffingByte
        #acknowledge do servidor para cliente confirmando recebimento 
        #correto do payload

    elif messageType == 6:
        head = int_to_byte(6,1)+payloadLen+EOP+stuffingByte
        #nacknowledge do servidor para cliente pedindo reenvio do pacote por 
        #erro de transmissão

    elif messageType == 7:
        head = int_to_byte(7,1)+payloadLen+EOP+stuffingByte
        #Pedido de encerramento da mensagem

    elif messageType == 8:
        head = int_to_byte(8,1)+payloadLen+EOP+stuffingByte
        #Erro tipo 1: cliente não recebeu mensagem tipo 2

    elif messageType == 9:
        head = int_to_byte(9,1)+payloadLen+EOP+stuffingByte
        #Erro tipo 2: servidor não recebeu mensagem tipo 3

    elif messageType == 0:
        head = int_to_byte(0,1)+payloadLen+EOP+stuffingByte
        #Erro tipo 3: não recebeu ack ou nack em 5 segundos

    else:
        head = None 
        #messageType fora do protocolo e portanto byte não deve ser formado com HEAD


    all = bytes()
    all += head
    all += payload
    all += EOP
    print("\n Head len:  ",len(head))

    return all



def readHeadNAll(receivedAll):

    head = receivedAll[0:21]

    txLen = fromByteToInt(head[1:6])

    messageType = fromByteToInt(head[0])
    #Leitura do messaType do pacote recebido


    eopSystem = head[6:18]
    print('END OF PACKAGE', eopSystem)
    stuffByte = head[18:22]

    sanityCheck = bytearray()
    stuffByteCount = 0

    for i in range(22, len(receivedAll)):
        if receivedAll[i:i+1] == stuffByte:
            sanityCheck += receivedAll[i+1:i+14]
            i +=14
        elif eopSystem == receivedAll[i:i+13]:
            print('EOP: 'receivedAll[i:i+13])
            break

        else:
            sanityCheck += receivedAll[i:i+1]


    print('SanityCheck ', sanityCheck)
    if len(sanityCheck) == txLen:

        print ("sanityCheck = okay")
        return sanityCheck, txLen, messageType

    '''
    ATENÇÃO: TROCAR ELSE POR TRATAMENTO DE ERROS VIA PROTOCOLO MESSAGETYPE

    '''

    # else:
    #     print ("\n\n ERRO  \n\n HOUVE FALHA NA TRANSMISSÃO. FECHANDO APLICAÇÃO… TENTE NOVAMENTE.")
    #     quit()




def teste():
    img = Image.open('circuit.jpg', mode='r')
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='JPEG')
    imgByteArr = imgByteArr.getvalue()
    testeSubject = encapsulate(imgByteArr)
    print('testeSubject 'testeSubject)
    txLenRead, txLenRead2 = readHeadNAll(testeSubject)

    print("\n Reading TxLen:     ",txLenRead )
    print("\n Reading Txlen: ", txLenRead2)
