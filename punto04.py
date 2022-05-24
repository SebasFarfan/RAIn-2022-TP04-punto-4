import lxml
from bs4 import BeautifulSoup
import pandas
import requests

url = "https://www.repository.cam.ac.uk/oai/request?verb=ListRecords&metadataPrefix=oai_dc"


def obtenerPeticionGet(url):
    '''
    Método que realiza una petición Get para obtener la pagina. 
    Arg: 
    url: [str]
    Return:
    website: [requests.Response] 
    '''
    peticion = requests.get(url)
    return peticion


def obtenerEstructuraXML(pagina):
    ''''
    Método que obtiene la estructura xml \n
    Arg: \n pagina: [request.Response] \n
    Return: \n metadata: [ResultSet]
    '''
    xmls = BeautifulSoup(pagina.content, features='xml')
    metadata = xmls('metadata')
    return metadata


def obtenerDatos(bloquesMetadatos):
    '''
    Método que en base un bloque xml obtiene una serie de datos
    como ser título, resumen, autores, palabras claves y fechas. \n
    Arg: \n bloqueMetadatos: [ResultSet] \n
    Return:\n lista100Registros: [list]
    '''
    lista100Registros = []
    cont = 0
    for etiqueta in bloquesMetadatos:
        listaContenido = []
        titulo = etiqueta.find('dc:title').getText()
        resumen = etiqueta.find_all('dc:description')
        textdescripcion = []
        for elemento in resumen:
            textdescripcion.append(elemento.text)
        autores = etiqueta.find_all('dc:creator')
        textoAutor = []
        for elemento in autores:
            textoAutor.append(elemento.text)
        palabrasClave = etiqueta.find_all('dc:subject')
        textoPalabraClave = []
        for elemento in palabrasClave:
            textoPalabraClave.append(elemento.text)
        fechas = etiqueta.find_all('dc:date')
        textoFechas = []
        for fecha in fechas:
            textoFechas.append(fecha.text)

        listaContenido.append(titulo)
        listaContenido.append(' - '.join(textdescripcion))
        listaContenido.append(' - '.join(textoAutor))
        listaContenido.append(' - '.join(textoPalabraClave))
        listaContenido.append(' - '.join(textoFechas))

        lista100Registros.append(listaContenido)
        cont += 1
    print(cont, 'Registros')
    return lista100Registros


def generarSalida(listaDatos):
    '''
    Método que en base a una lista de datos genera un archivo en formato 'csv'. \n
    Arg: \n listaDatos: [list] \n
    '''
    print('-'*10, 'Generando archivo de salida', '-'*10)
    listaTit = []
    listaResumen = []
    listaAutores = []
    listaPalabraClaves = []
    listaFechas = []
    for lista in listaDatos:
        listaTit.append(lista[0])
        listaResumen.append(lista[1])
        listaAutores.append(lista[2])
        listaPalabraClaves.append(lista[3])
        listaFechas.append(lista[4])
    diccionarioDatos = {'Titulo': listaTit, 'Resumen': listaResumen, 'Autores': listaAutores, 
                        'Palabra Clave': listaPalabraClaves, 'Fechas': listaFechas}
    df = pandas.DataFrame(diccionarioDatos)
    df.to_csv('salida2.csv')
    print('-'*10, 'Se generó el archivo salida.csv', '-'*10)


# --------------------- Principal ---------------------

# obtiene la petición get HTTP
print('Realizando petición HTTP')
peticionHTTP = obtenerPeticionGet(url)

# si otiene petición realiza obtenecion del bloque especifico
print('Obteniendo bloque de metadatos ')
bloquemetadatos = obtenerEstructuraXML(peticionHTTP)

# extrae datos del bloque título, resumen, autores, palabras claves, fechas
print('Extrayendo datos ---')
listaDatos = obtenerDatos(bloquemetadatos)

# almacena en un archivo .csv
generarSalida(listaDatos)
