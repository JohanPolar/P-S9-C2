import boto3
from bs4 import BeautifulSoup
import datetime


paginas = [
    ('El_Espectador', 'https://www.elespectador.com/'),
    ('Publimetro', 'https://www.publimetro.co/'),
    ('El_Tiempo', 'https://www.eltiempo.com')
]


def obtenerA():
    date = datetime.datetime.now()
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('parcialnews')

    objects = []

    for name in paginas:
        obj = bucket.Object(f'headlines/raw/{name[0]}-{date.strftime("%Y-%m-%d")}.html')
        body = obj.get()['Body'].read()
        objects.append(body)

    return objects


def csv_parse(info):
    csv_acum = "categoria, titulo, link\n"
    for row in info:
        csv_acum += row[0]
        csv_acum += ", "

        csv_acum += row[1]
        csv_acum += ", "

        csv_acum += row[2]
        csv_acum += "\n"
    return csv_acum


def get_info_elespectador(object):
    newspaper = "elespectador.com"
    soup = BeautifulSoup(object, features="lxml")

    information = []

    data = soup.find_all('div', attrs={'class': 'Card-Container'})
    category = data[0].find_all('h4', attrs={'class': 'Card-Section Section'})
    try:
        category = category[0].find_all('a')[0].contents[0]
    except:
        category = ""
    title = data[0].find_all('h2', attrs={'class': 'Card-Title Title Title_main'})
    link = newspaper
    link += title[0].find_all('a', href=True)[0]['href']
    title = title[0].find_all('a')[0].contents[0]
    title = title.replace(",", "")
    category = category.replace(",", "")
    link = link.replace(",", "")
    information.append((category, title, link))

    columna_central = soup.find_all('section', attrs={'class': 'Layout-mainHomeA'})

    columna_central = soup.find_all('div', attrs={'class': 'Card-Container'})

    for element in columna_central:

        try:
            category = element.find_all('h4', attrs={'class': 'Card-Section Section'})
            category = category[0].find_all('a')[0].contents[0]
        except:
            category = ""

        title = element.find_all('h2', attrs={'class': 'Card-Title Title Title'})
        link = newspaper
        try:
            link += title[0].find_all('a', href=True)[0]['href']
        except:
            link = ""

        try:
            title = title[0].find_all('a')[0].contents[0]
        except:
            title = ""
        title = title.replace(",", "")
        category = category.replace(",", "")
        link = link.replace(",", "")
        information.append((category, title, link))

    return csv_parse(information)


def get_info_publimetro(object):
    newspaper = "https://www.publimetro.co"
    soup = BeautifulSoup(object, features="lxml")
    information = []

    main = soup.find_all('article', attrs={'class': 'container-fluid xl-large-promo'})
    title = main[0].find_all('a', attrs={'class': 'xl-promo-headline'})[0].contents[0]
    link = newspaper
    link += main[0].find_all('a', attrs={'class': 'xl-promo-headline'}, href=True)[0]['href']
    category = ""

    title = title.replace(",", "")
    category = category.replace(",", "")
    link = link.replace(",", "")
    information.append((category, title, link))

    news = soup.find_all('div', attrs={'class': 'card-list-container'})
    for element in news:
        try:
            category = element.find_all('span', attrs={'class': 'primary-font__PrimaryFontStyles-o56yd5-0 ctbcAa overline card-list-overline'})[0].contents[0]
        except:
            category = ""

        try:
            title = element.find_all('h2', attrs={'class': 'primary-font__PrimaryFontStyles-o56yd5-0 ctbcAa card-list-headline'})
            title = title[0].find_all('a', attrs={'class': 'list-anchor vertical-align-image'})[0].contents[0]

        except:
            title = ""

        try:
            link = newspaper
            link_1 = element.find_all('h2', attrs={'class': 'primary-font__PrimaryFontStyles-o56yd5-0 ctbcAa card-list-headline'})
            link += link_1[0].find_all('a', attrs={'class': 'list-anchor vertical-align-image'}, href=True)[0]['href']
        except:
            link = ""
        title = title.replace(",", "")
        category = category.replace(",", "")
        link = link.replace(",", "")
        information.append((category, title, link))

    return csv_parse(information)


def get_info_eltiempo(object):
    newspaper = "eltiempo.com"
    soup = BeautifulSoup(object, features="lxml")

    information = []

    data = soup.find_all('div', attrs={'class': 'article-details'})

    for element in data[:7]:

        try:
            category = element.find_all('div', attrs={'class': 'category-published'})
            category = category[0].find_all('a')[0].contents[0]
        except:
            category = ""

        title = element.find_all('h3', attrs={'class': 'title-container'})
        link = newspaper
        try:
            link += title[0].find_all('a', href=True)[0]['href']
        except:
            link = ""

        try:
            title = title[0].find_all('a')[0].contents[0]
        except:
            title = ""
        title = title.replace(",", "")
        category = category.replace(",", "")
        link = link.replace(",", "")
        information.append((category, title, link))

    for element in data[7:]:

        try:
            category = element.find_all('div', attrs={'class': 'category-published'})
            category = category[0].find_all('a')[0].contents[0]
        except:
            category = ""

        title = element.find_all('h2', attrs={'class': 'title-container'})
        link = newspaper
        try:
            link += title[0].find_all('a', href=True)[0]['href']
        except:
            link = ""

        try:
            title = title[0].find_all('a')[1].contents[0]
        except:
            title = ""
        title = title.replace(",", "")
        category = category.replace(",", "")
        link = link.replace(",", "")
        information.append((category, title, link))

    return csv_parse(information)


def upload_csv(files):
    print("Getting files")
    csv_acum = get_info_elespectador(files[0])
    client = boto3.client('s3')
    print("Uploading ", paginas[0][0])
    client.put_object(Body=csv_acum, Bucket='parcialnews',
                      Key=f'headlines/final/periodico={paginas[0][0]}/year={datetime.datetime.now().year}/month={datetime.datetime.now().month}/day={datetime.datetime.now().day}/{paginas[0][0]}-{datetime.datetime.now().strftime("%Y-%m-%d")}.csv')

    csv_acum = get_info_publimetro(files[1])
    print("Uploading ", paginas[1][0])
    client.put_object(Body=csv_acum, Bucket='parcialnews',
                      Key=f'headlines/final/periodico={paginas[1][0]}/year={datetime.datetime.now().year}/month={datetime.datetime.now().month}/day={datetime.datetime.now().day}/{paginas[0][0]}-{datetime.datetime.now().strftime("%Y-%m-%d")}.csv')

    csv_acum = get_info_eltiempo(files[2])
    print("Uploading ", paginas[2][0])
    client.put_object(Body=csv_acum, Bucket='parcialnews',
                      Key=f'headlines/final/periodico={paginas[2][0]}/year={datetime.datetime.now().year}/month={datetime.datetime.now().month}/day={datetime.datetime.now().day}/{paginas[0][0]}-{datetime.datetime.now().strftime("%Y-%m-%d")}.csv')


objects = obtenerA()

upload_csv(objects)
