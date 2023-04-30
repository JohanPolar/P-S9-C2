import boto3

# Configurar el cliente de S3
s3 = boto3.client('s3')

# Nombre del archivo que se desea subir
file_name = 'parcial2.py'

# Nombre del bucket donde se guardará el archivo
bucket_name = 'aws-glue-assets-290086197854-us-east-1'

# Nombre de la carpeta dentro del bucket donde se guardará el archivo
folder_name = 'scripts'

# Ruta completa del archivo que se subirá al bucket
file_path = f'{folder_name}/{file_name}'

# Subir archivo al bucket
with open(file_name, 'rb') as f:
    s3.upload_fileobj(f, bucket_name, file_path)

# Nombre del archivo que se desea subir
file_name = 'parcial2all.py'

# Ruta completa del archivo que se subirá al bucket
file_path = f'{folder_name}/{file_name}'

# Subir archivo al bucket
with open(file_name, 'rb') as f:
    s3.upload_fileobj(f, bucket_name, file_path)