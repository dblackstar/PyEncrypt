from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time

class Encriptador:

    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encriptar(self, mensaje, key, key_size = 256):
        mensaje = self.pad(mensaje)
        iv = Random.new().read(AES.block_size) # Vector de inicializacion
        cifrado = AES.new(key, AES.MODE_CBC, iv) # Tipo de cifrado
        return iv + cifrado.encrypt(mensaje)
    
    def encriptar_archivo(self, nombreDeArchivo):
        with open(nombreDeArchivo, 'rb') as fo: # rb = leer en binario
            textoPlano = fo.read()
        enc = self.encriptar(textoPlano, self.key)
        with open(nombreDeArchivo + ".enc", 'wb') as fo: # wb = escrbir en binario
            fo.write(enc)
        os.remove(nombreDeArchivo)  

    def decifrar(self, textoCifrado, key):
        iv = textoCifrado[:AES.block_size]
        cifrado = AES.new(key, AES.MODE_CBC, iv)
        textoPlano = cifrado.decrypt(textoCifrado[AES.block_size:])
        return textoPlano.rstrip(b"\0")
    
    def decifrar_archivo(self, nombreDeArchivo):
        with open(nombreDeArchivo, 'rb') as fo:
            textoCifrado = fo.read()
        dec = self.decifrar(textoCifrado, self.key)
        with open(nombreDeArchivo[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(nombreDeArchivo)

key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
enc = Encriptador(key)
clear = lambda: os.system('cls')

if os.path.isfile('datos.txt.enc'):

    while True:
        clave = str(input("Ingresa la contraseña: "))
        enc.decifrar_archivo("datos.txt.enc")
        p = ''
        with open("datos.txt", "r") as f:
            p = f.readlines()
        if p[0] == clave:
            enc.encriptar_archivo("datos.txt")
            break

    while True:
        clear()
        opcion = int(input("1. Presiona '1' para encriptar un archivo.\n2. Presiona '2' para decifrar un archivo.\n3. Presiona '3' para salir.\n"))
        clear()
        if opcion == 1:
            enc.encriptar_archivo(str(input("Ingresa el nombre o arrastra el archivo que quieras encriptar: ")))
        elif opcion == 2:
            enc.decifrar_archivo(str(input("Ingresa el nombre o arrastra el archivo cifrado: ")))
        elif opcion == 3:
            exit()
        else:
            print("Selecciona una opcion valida")

else:
    while True:
        clear()
        clave = str(input("Ingresa la contraseña que se usara para el cifrado: "))
        reclave = str(input("Confirma la contraseña: "))
        if clave == reclave:
            break
        else:
            print("Las contraseñas no coinciden")
    f = open("datos.txt", "w+")
    f.write(clave)
    f.close()
    enc.encriptar_archivo("datos.txt")
    print("Reinicia el programa")
    time.sleep(10)