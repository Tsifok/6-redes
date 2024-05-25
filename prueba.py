from sql_exer.config import *

conexion = obtener_conexion()
email = "test@gmail.com"
password = "test"

cursor = conexion.cursor()
consulta = f'SELECT * FROM usuarios WHERE email = "{email}" AND password = "{password}"'
cursor.execute(consulta)
resultado = cursor.fetchone()
print(resultado[0])
