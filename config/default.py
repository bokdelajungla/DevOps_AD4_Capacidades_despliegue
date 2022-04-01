# *** VARIABLES *** #

# Nombre del fichero de persistencia
FILENAME = "cadenas.txt" #Fichero por defecto

# Host
HOST = "127.0.0.1"

# Puerto
PORT = 12345 #Puerto por defecto

# Configuración Base de Datos
SECRET_KEY = '26e6f5689c2c07c42e85e725dcda798088cf673d3141bd17dfe3ef688457c351'
SQLALCHEMY_DATABASE_URI = 'sqlite:///devops_a4.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True