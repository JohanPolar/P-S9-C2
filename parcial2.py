import boto3
import urllib.request
from datetime import datetime


def capture_data():
    session = boto3.Session()
    s3 = session.resource('s3')
    bucket = s3.Bucket('parcialnews')
    date = datetime.now().strftime("%Y-%m-%d")
    response = urllib.request.urlopen('https://www.elespectador.com/')
    webContent = response.read()
    bucket.put_object(Body=webContent, Key='headlines/raw/{}-{}.html'
                      .format('El_Espectador', date))
    response = urllib.request.urlopen('https://www.publimetro.co/')
    webContent = response.read()
    bucket.put_object(Body=webContent, Key='headlines/raw/{}-{}.html'
                      .format('Publimetro', date))
    response = urllib.request.urlopen('https://www.eltiempo.com/')
    webContent = response.read()
    bucket.put_object(Body=webContent, Key='headlines/raw/{}-{}.html'
                      .format('El_Tiempo', date))


capture_data()
