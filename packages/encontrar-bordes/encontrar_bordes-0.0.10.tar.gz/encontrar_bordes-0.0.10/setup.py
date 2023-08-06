import pathlib
from setuptools import find_packages, setup

#dudo de esta linea
HERE = pathlib.Path(__file__).parent

VERSION = '0.0.10' 
PACKAGE_NAME = 'encontrar_bordes'
AUTHOR = 'Paul Andres Romero Coronado <paulssj14@gmail.com>' + 'Pablo Ezequiel Cordoba <ezequielcordoba39@gmail.com>'
AUTHOR_EMAIL = 'paulssj14@gmail.com','ezequielcordoba39@gmail.com'
#AUTHOR_EMAIL = 'ezequielcordoba39@gmail.com'
#colocar la de github
URL = 'https://github.com/Ezequiel2003/UNSL---Proyecto-DSP2---Cordoba-Romero'

LICENSE = 'UNSL'
DESCRIPTION = 'Librería para extraer los contornos de una imagen, mostrarla y graficarla sobre la imagen original'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') #Referencia al documento README con una descripción más elaborada
LONG_DESC_TYPE = "text/markdown"

#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
      'cv2','numpy'
      ]
	  
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    #author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)
