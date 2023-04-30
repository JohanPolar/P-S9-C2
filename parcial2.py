import sys 
import boto3 
import urllib.request 
from datetime import datetime  

content_todownload = [('El_Espectador', 'https://www.elespectador.com/'),     
                      ('Publimetro', 'https://www.publimetro.co/'),     
                      ('El_Tiempo', 'https://www.eltiempo.com/')]

session = boto3.Session()
s3 = session.resource('s3')
bucket = s3.Bucket('parcialtiempo')

date = datetime.now().strftime("%Y-%m-%d")
for name, url in content_todownload:     
    response = urllib.request.urlopen(url)     
    webContent = response.read().decode('UTF-8')     
    bucket.put_object(Body=webContent, Key='headlines/raw/{}-{}.html'.format(name, date))