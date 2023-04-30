import unittest.mock as mock
import boto3
from moto import mock_s3
from datetime import datetime
from parcial2 import capture_data


@mock.patch('urllib.request.urlopen')
@mock_s3
def test_capture_data(mock_urlopen):
    # Configurar una conexión de prueba con S3
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='parcialnews')

    # Definir el contenido de ejemplo de las páginas web
    mock_urlopen.side_effect = [
        mock.mock_open(read_data='Ejemplo contenido El Espectador').return_value,
        mock.mock_open(read_data='Ejemplo contenido Publimetro').return_value,
        mock.mock_open(read_data='Ejemplo contenido El Tiempo').return_value
    ]

    # Ejecutar la función capture_data()
    capture_data()

    # Verificar que los objetos se hayan creado en el cubo S3
    bucket = conn.Bucket('parcialnews')
    date = datetime.now().strftime("%Y-%m-%d")
    keys = [obj.key for obj in bucket.objects.all()]
    expected_keys = [
        'headlines/raw/El_Espectador-{}.html'.format(date),
        'headlines/raw/El_Tiempo-{}.html'.format(date),
        'headlines/raw/Publimetro-{}.html'.format(date)
    ]
    assert keys == expected_keys
