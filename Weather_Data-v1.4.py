import requests
import pprint
import snap7
from time import sleep
from PIL import Image, ImageDraw, ImageFont, Image

#Fazer para milímetros

def imgday(dia,clima):

    #Organizar tipo de clima por imagem
###############################################################
    #if clima == 2,3,5,10,15,16,19,25,26:
    if clima in (2,3,5,10,15,16,19,25,26):
        dia = 0
        if clima in (2,15,19):
            clima = '00'  #0.png da pasta Neutro(dia=0)
        if clima == 25:
            clima = '01'  #1.png da pasta Neutro(dia=0)
        if clima in (10,26):
            clima = '02'  #2.png da pasta Neutro(dia=0)
        if clima == 5:
            clima = '03'  #3.png da pasta Neutro(dia=0)
        if clima in (3,16):
            clima = '04'  #4.png da pasta Neutro(dia=0)
################################################################
    if dia == 1:    
        if clima in (0,6):
            clima = 10   #10.png da pasta Lua
        elif clima in (14,23):
            clima = 11   #11.png da pasta Lua
        elif clima in (1,8):
            clima = 12   #12.png da pasta Lua
        elif clima in (7,13,15):
            clima = 13   #13.png da pasta Lua
        elif clima in (9,11,12,17,18,20,21,22,24,27):
            clima = 14   #14.png da pasta Lua
        elif clima in (4,10,28):
            clima = 15   #15.png da pasta Lua
        else:
            dia = 3
            clima = 0
################################################################
    if dia == 2:
        if clima in (0,6):
            clima = 20   #0.png da pasta Sol
        elif clima in (14,23):
            clima = 21   #1.png da pasta Sol
        elif clima in (1,8):
            clima = 22   #2.png da pasta Sol
        elif clima in (7,13,15):
            clima = 23   #3.png da pasta Sol
        elif clima in (9,11,12,17,18,20,21,22,24,27):
            clima = 24   #4.png da pasta Sol
        elif clima in (4,10,28):
            clima = 25   #5.png da pasta Sol
        else:
            dia = 3
            clima = 0


    if dia == 1 or 2:
        image = Image.open(r'Q:/Servicos Tecnicos/Data/Desenvolvimento/Miscelâneas/vclouds_weather_icons_by_vclouds_d2ynulp/VClouds Weather Icons/Usable/' + str(clima) + '.png')
    elif dia == 3:
        image = Image.open(r'Q:/Servicos Tecnicos/Data/Desenvolvimento/Miscelâneas/vclouds_weather_icons_by_vclouds_d2ynulp/VClouds Weather Icons/Usable/40.png')

    foto = str(clima) 

    #image.show()
    #image.close()
    return(foto)


def extractweatherdata():
    r = requests.get('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/-22.879503938580836%2C%20-43.288833943295224?unitGroup=metric&key=6CUR7X99GULRDNPEUJH3JQB4E&include=fcst%2Ccurrent')
    print(r)
    data =r.json()
    dataday = data['days'][0]
    currentconditions = data['currentConditions']

    clima = currentconditions['icon']
    precipitação = int(dataday['precip'])
    precprob = int(dataday['precipprob'])
    temperatura = int(currentconditions['temp'])
    umidade = int(currentconditions['humidity'])
    vento = int(currentconditions['windspeed'])
    dirvento = int(currentconditions['winddir'])
    condicoes = currentconditions['conditions']
    sunrise = currentconditions['sunrise']
    sunset = currentconditions['sunset']
    time = currentconditions['datetime']

    pprint.pprint(currentconditions)
    #print(precipitação)
    #print(precprob)


    if (time >= sunrise and time <= sunset):
        dia = 2                    #manhã = 2
    if(time<= sunrise or time >= sunset):
        dia = 1                    #tarde = 1


    #pprint.pprint(currentconditions)
    clima = condicoes

    writePLC(clima,temperatura,umidade,vento,precipitação,precprob,dia)


def writePLC(cstatus,temp,umid,vento,chuva,probchuva,dia):
    IP = '10.20.19.250'    #selecionar IP do PLC   #10.20.19.250
    RACK = 0
    SLOT = 1


    DB_NUMBER = 5
    START_ADRESS = 0
    SIZE =2                     #adicionar 2 a mais por conta de um byte extra do PLC(start byte) + o 0
    #Colocar variável clima

    #dicionario
    dic_tempo = {
        'Clear':0,                                      #Céu limpo
        'Partially cloudy':1,                           #Parcialmente nublado
        'Overcast':2,                                   #Nublado
        'Hail':3,                                       #Chuva de granizo
        'Thunderstorm Without Precipitation':4,         #Trovoadas sem chuva
        'Thunderstorm':5,                               #Tempestade
        'Sky Unchanged':6,                              #Céu sem mudanças
        'Sky Coverage Increasing':7,                    #Índice de nuvens aumentando
        'Sky Coverage Decreasing':8,                    #Índice de nuvens abaixando  
        'Light Rain':9,                                 #Chuva leve
        'Heavy Rain':10,                                #Chuva pesada
        'Rain Showers':11,                              #Chuva de verão
        'Rain':12,                                      #Chuva
        'Precipitation In Vicinity':13,                 #Chuva nas proximidades
        'Mist':14,                                      #Névoa
        'Lightning Without Thunder':15,                 #Raio sem trovoada
        'Hail Showers':16,                              #Chuva de granizo
        'Light Freezing Rain':17,                       #Chuva leve fria
        'Heavy Freezing Rain':18,                       #Chuva forte fria
        'Freezing Fog':19,                              #Vento frio
        'Light Freezing Drizzle/Freezing Rain':20,      #Chuvisco leve frio
        'Heavy Freezing Drizzle/Freezing Rain':21,      #Chuvisco forte frio
        'Freezing Drizzle/Freezing Rain':22,            #Chuvisco frio
        'Fog':23,                                       #Névoa
        'Drizzle':24,                                   #Chuvisco
        'Light Drizzle/Rain':25,                        #Chuvisco leve/Chuva 
        'Heavy Drizzle/Rain':26,                        #Chuvisco forte/Chuva
        'Light Drizzle':27,                             #Chuvisco leve
        'Heavy Drizzle':28,                             #Chuvisco forte


    }

    img = imgday(dia,dic_tempo[cstatus])
    #print(img)
    img = '  ' + img                           #transforma em bytes
    img = bytes(img, 'utf-8')

    #Dicionario img:
    #Primeiro valor = dia       0 = Nuvens(depende apenas do clima)     1 = Lua     2 = Sol
    #Segundo valor = clima      
    #Para dia = Sol ou Lua, clima: 0 = Limpo  1 = levemente nublado  2 = Nublado  3 = Muito nublado  4 = Chuva  5 = Muita Chuva(possivelmente com trovoadas)
    #Para dia = Nuvens, clima: 0 = Nublado  1 = Chuva leve  2 = Chuva pesada  3 = Chuva com raios  4 = Chuva com granizo

  
    if int(str(dic_tempo[cstatus])) <=9:
        cstatus = '  0' + str(dic_tempo[cstatus])
    else:
        cstatus = ' ' + str(dic_tempo[cstatus])

    cstatus = bytes(cstatus, 'utf-8')

    if int(chuva)>=10:
        if int(chuva)>99:
            chuva = 99
        chuva = '  ' + str(chuva)                           #transforma em bytes
        chuva = bytes(chuva, 'utf-8')
    else:
        chuva = '  0' + str(chuva)                           #transforma em bytes
        chuva = bytes(chuva, 'utf-8')

    if int(probchuva)>=10:
        if int(probchuva)>99:
            probchuva = 99
        probchuva = '  ' + str(probchuva)                           #transforma em bytes
        probchuva = bytes(probchuva, 'utf-8')
    else:
        probchuva = '  0' + str(probchuva)                           #transforma em bytes
        probchuva = bytes(probchuva, 'utf-8')

    if int(temp)>=10:
        temp = '  ' + str(temp)                           #transforma em bytes
        temp = bytes(temp, 'utf-8')
    else:
        temp = '  0' + str(temp)                           #transforma em bytes
        temp = bytes(temp, 'utf-8')

    if int(umid)>=10:
        umid = '  ' + str(umid)                           #transforma em bytes
        umid = bytes(umid, 'utf-8')
    else:
        umid = '  0' + str(umid)                           #transforma em bytes
        umid = bytes(umid, 'utf-8')

    if int(vento)>=10:
        vento = '  ' + str(vento)                           #transforma em bytes
        vento = bytes(vento, 'utf-8')
    else:
        vento = '  0' + str(vento)                           #transforma em bytes
        vento = bytes(vento, 'utf-8')


    plc = snap7.client.Client()   #seleciona o PLC
    plc.connect(IP,RACK,SLOT)

    plc_info = plc.get_cpu_info()  #imprime informação do modelo do PLC
    print(f'Module Type: {plc_info.ModuleTypeName}')

    print(plc.get_cpu_state())  #imprime o estado do PLC (se esta rodando ou com erro)

    db = plc.db_read(DB_NUMBER, START_ADRESS, SIZE)
    print(db)                   #mostra todos os bytes(incluindo o start byte) que podem ser utilizados

    #Os dados abaixo são variáveis e parâmetros programados direto no PLC que podemos utilizar o snap7 para ler pelo computador. No plc as variáveis seriam algo como: "Interface".product_name := 'Snap7 PLC to App';
    #Quando printarmos essa variável especificada anteriormente neste programa, ela leria exatamente 'Snap7 PLC to App'

    product_name = db[2:256].decode('UTF-8').strip('\x00')    #utilizar do segundo byte(primeiro que é utilizável) até o 256. Depois os zeros são cortados para ficar mais legível em python
    print(product_name)

    #product_value = int.from_bytes(db[256:258], byteorder='big')   #Pega os bytes de 256 a 258 e mostra parâmetros de rastreabilidade, como hora da montagem, força de prensagem, curso de prensagem... É possível criar um objeto e jogar a informação num banco de dados
    #print(product_value)

    #product_status = bool(db[258])
    #print(product_status)

    #Escrevendo na Ddb
    #print(chuva)
    print(cstatus,temp,umid,vento,probchuva,chuva,img)

    plc.db_write(DB_NUMBER, 0, cstatus)
    plc.db_write(DB_NUMBER, 4, temp)
    plc.db_write(DB_NUMBER, 8, umid)
    plc.db_write(DB_NUMBER, 12, vento)   
    plc.db_write(DB_NUMBER, 16, probchuva)
    plc.db_write(DB_NUMBER, 20, chuva)
    plc.db_write(DB_NUMBER, 24, img)

    #serão inteiros ex: 0 a 5 - 0 sol; 1 chuva...
    #national instruments
    print("Clima:" + (str(cstatus)[3:6]))
    print("Temperatura:" + (str(temp)[3:6]) + "°C")
    print("Umidade:" + (str(umid)[3:6]) + "%")
    print("Velocidade do vento:" + (str(vento)[3:6]) + "km/h")
    print("Probabilidade de chuva:" + (str(probchuva)[3:6]) + "%")
    print("Chuva:" + (str(chuva)[3:6]) + "mm")
    print("Imagem:" + (str(img)[3:6]))

while True:

    try:
        extractweatherdata()
    except Exception as e:
        print(e)
    sleep(1200)        



extractweatherdata()