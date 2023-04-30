<p align="center">
<FONT FACE="times new roman" SIZE=5>
<br>
Ciencias de la computación e inteligencia artificial
<br>
<i><b>Big Data e Ingeniería de Datos</b></i>
<br>
<img src="https://res-5.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_256,w_256,f_auto,q_auto:eco/v1455514364/pim02bzqvgz0hibsra41.png"
width="150" height="150">
</img>
<br>
<i><b>Docente:</b></i><br> Camilo Rodriguez
<br>
<i><b>Autores:</b></i>
<br>
Johan Moreno
<br>
Erika Romero
<br>

# Parcial 2
Este proyecto tiene como objetivo realizar web scraping en tres sitios web: https://www.elespectador.com/, https://www.publimetro.co/, y https://www.eltiempo.com/. Esto se logra mediante el uso de la biblioteca BeautifulSoup en Python y AWS Glue Jobs en la plataforma AWS. El objetivo es extraer información de noticias y guardarla en un archivo CSV.

Se ha creado un pipeline de despliegue continuo utilizando GitHub Actions y un flujo de trabajo de AWS que se ejecuta diariamente para extraer noticias de los tres sitios web. Las noticias se almacenan en un bucket S3 particionado según el nombre del sitio web ("periodico"), el año, mes y día en que se adquirió la información ("year", "month", "day"). La información escaneada se sube a una base de datos MySQL en RDS, donde está lista para su uso en diferentes consultas.

## Requerimientos
#### Cuenta AWS CLI
| Buckets S3 |  
| :-------- | 
|  S3 -> bucket: "parcialnews"|
|  RDS -> database: "parcial" |

* Python 3.9
* Boto3
* BeautifulSoup
* Pytest
* moto (prueba unitaria test_parcial2all.py)
* Y demás se encuentran en los diferentes archivos requirements.txt


## Instalación

Clonación del repositorio, e ingrese a la carpeta creada

```bash
  git clone git@github.com:JohanPolar/PARCIAL-BD.git
  cd PARCIAL-BD/
```
    
De preferencia tener un enviroment para que las dependencias se intalen de manera correcta y no hayan complicaciones, esto se puede generar por medio de:

```bash
    virtualenv -p python3.9 env
```
Activar el environment creado 
```bash
    source env/bin/activate
```
Instalación de requirements 
```bash
    pip install -r requierements.txt
```

Configuración de sus credenciales dentro de un archivo en una carpeta .aws situada en la raiz llamado credentials. 
  
# Desarrollo
  
El proyecto en total cuenta con:

El objetivo de este proyecto es realizar web scraping a tres sitios web diferentes: https://www.elespectador.com/, https://www.publimetro.co/, y https://www.eltiempo.com/. Para ello se utilizan las funciones de BeautifulSoup en Python, a través de los Jobs de AWS Glue en la plataforma AWS, con el fin de extraer la información de las noticias y guardarla en un archivo CSV.

El proyecto cuenta con:

* Un pipeline de despliegue continuo en Github que ejecuta las pruebas unitarias y una revisión léxica por medio de Flake8 al actualizar los scripts de los Jobs usados.

* Un Job1 con un Trigger que se ejecuta diariamente para adquirir la información de los tres sitios web mencionados.

* La información adquirida es almacenada en un bucket S3 en formato .html.
    
* El pipeline de despliegue continuo de AWS se activa automáticamente justo después de que finalice el Job1, permitiendo que se active el Job2, el cual procesa la información almacenada para guardar el archivo CSV en una carpeta adyacente del directorio.
    
* Al finalizar el crawler1, se actualiza el catálogo de AWS Glue que permite visualizar los datos almacenados en AWS Athena.
    
* Por último, la ejecución del crawler2 permite el escaneo y creación de una nueva tabla en AWS Glue que se extrae de RDS, con el fin de ser compatibles con los datos enviados a RDS a través de dicha tabla. De esta manera, se termina dentro de la base de datos preparada para realizar consultas de manera eficiente.

Los resultados se pueden observar en el siguiente link: https://docs.google.com/document/d/1ceelrxlIoLL2XlR2TA3sU5ugjfLSWHdkgz2aLnC3r9w/edit?usp=sharing

#### TENER EN CUENTA:
Se debe cambiar las variables privadas de GitHubActions, para que tenga el acceso a su cuenta de AWS y pueda realizar todas las acciones respectivas

## Insignias

[![Flake8 License](https://img.shields.io/badge/License-Flake8-orange)](https://github.com/PyCQA/flake8/blob/main/LICENSE)

[![Pytest License](https://img.shields.io/badge/License-Pytest-red)](https://docs.pytest.org/en/7.1.x/license.html)

## Autores

- [@Johan Moreno](https://github.com/JohanPolar)
- [@Erika Romero](https://github.com/erika-romero)
