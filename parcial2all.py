import json
import boto3
from datetime import datetime
import datetime as dt
from bs4 import BeautifulSoup

def csv_parse(info):
    csv_acum = "categoria, titulo, link\n"
    for row in info:
        csv_acum+=row[0]
        csv_acum+=", "

        csv_acum+=row[1]
        csv_acum+=", "

        csv_acum+=row[2]
        csv_acum+="\n"
    return csv_acum

def get_objects(pagina):

    date = datetime.now()+ dt.timedelta(hours=5)
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('parcialtiempo')

    objects = []

    content_todownload = [('El_Espectador', 'https://www.elespectador.com/'),     
                      ('Publimetro', 'https://www.publimetro.co/'),     
                      ('El_Tiempo', 'https://www.eltiempo.com/')]

    name = content_todownload[pagina]
    obj = bucket.Object(f'/headlines/raw/{name[0]}-{date.strftime("%Y-%m-%d")}.html')
    body = obj.get()['Body'].read()
    return body

def proccesing_data_elespectador():
    newspaper = "elespectador.com"
    soup = BeautifulSoup(get_objects(0), features="lxml")

    information =[]

    #Titular principal
    data = soup.find_all('div', attrs={'class': 'Card-Container'})
    category = data[0].find_all('h4', attrs={'class': 'Card-Section Section'})
    category = category[0].find_all('a')[0].contents[0]
    title = data[0].find_all('h2', attrs={'class': 'Card-Title Title Title_main'})
    link = newspaper
    link += title[0].find_all('a', href = True)[0]['href']
    title = title[0].find_all('a')[0].contents[0]

    information.append((category, title, link))

    #Columnas
    columna_central = soup.find_all('section', attrs={'class': 'Layout-mainHomeA'})
    
    columna_central = soup.find_all('div', attrs={'class': 'Card-Container'})

    print(len(columna_central))

    for element in columna_central:
        #Card-Section Section

        try:
            category = element.find_all('h4', attrs={'class': 'Card-Section Section'})
            category = category[0].find_all('a')[0].contents[0]
        except:
            category = ""
        
        title = element.find_all('h2', attrs={'class': 'Card-Title Title Title'})
        link = newspaper
        try:
            link += title[0].find_all('a', href = True)[0]['href']
        except:
            link = ""
            
        try:
            title = title[0].find_all('a')[0].contents[0]
        except:
            title = ""

        information.append((category, title, link))

    return csv_parse(information)

def proccesing_data_el_tiempo():
    body = get_objects(2)
    soup = BeautifulSoup(body, 'html.parser')
    data_casas = soup.find_all('div', class_='listing listing-card')
    data_barrio = soup.find_all('div', class_='listing-card__location')
    data_precio = soup.find_all('div', class_='price')

    print(format)

    csv = "FechaDescarga, Barrio, Valor, NumHabitaciones, NumBanos, mts2\n"

    for i in range(len(data_casas)):
        download_date = now.strftime('%d-%m-%Y')
        barrio = (data_barrio[i].text)
        newBarrio = ""
        for j in barrio:
            newBarrio += j
        barrio = newBarrio.replace(',', '.')
        price = (data_precio[i].text)
        num_rooms = (f"{data_casas[i]['data-rooms']}")
        num_BRooms = (f"{data_casas[i].find_all('div', class_='listing-card__properties')[0].find_all('span')[1].text[:1]}")
        mts = (f"{data_casas[i].find_all('div', class_='listing-card__properties')[0].find_all('span')[2].text}")
        csv += f"{download_date}, {barrio}, {price}, {num_rooms}, {num_BRooms}, {mts}\n"

    client = boto3.client("s3")
    client.put_object(Body=csv, Bucket="casas-final-3003", Key='' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '.csv')
    return {
        'statusCode': 202,
        'body': json.dumps('Hello from Lambda!')
    }



def get_objects(pagina):

    date = datetime.now()+ dt.timedelta(hours=5)
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('parcialtiempo')

    objects = []

    content_todownload = [('El_Espectador', 'https://www.elespectador.com/'),     
                      ('Publimetro', 'https://www.publimetro.co/'),     
                      ('El_Tiempo', 'https://www.eltiempo.com/')]

    name = content_todownload[pagina]
    obj = bucket.Object(f'/headlines/raw/{name[0]}-{date.strftime("%Y-%m-%d")}.html')
    body = obj.get()['Body'].read()
    return body

now = datetime.now()
csv_espectador = proccesing_data_elespectador()
client = boto3.client("s3")
client.put_object(Body=csv_espectador, Bucket="parcialtiempo", Key="/headlines/final/periodico=El_espectador/year=" + str(now.year) + "/month="+str(now.month)+"/day="+str(now.day) + ".csv")