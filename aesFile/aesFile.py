# Universidad del Valle de Guatemala
# Cifrado de información
# Grupo 7
# Implementación 2 AES

# INSTRUCCIONES
# Implementar un programa permite el cifrado de un documento cualquiera (txt, pdf, etc). Asegúrese de
# especificar sobre cúal tipo de archivo funcionará. Tome en cuenta que deberá mostrar cómo se ve el
# archivo cifrado y descifrado. Además ustedes deberán:
# a. Comentar correctamente cada paso que está realizando en su código

# b. Responda (como comentario de bloque dentro del mismo código)
# i. ¿Qué modo de AES usó? ¿Por qué?
# El modo de AES utilizado fue MODE_GCM Galois/Counter Mode (GCM).
# Realmente nos llevo a implementarlo que lo investigamos durante este laboratorio y por tanto, deseabamos probarlo.
# Una gran ventaja es que tiene un buen rendimiento y eficiencia.
# Tiene una latencia mínima y su sobrecarga de funcionamiento es muy poca.
# Básicamente este funciona con bloques numerados secuencialmente y se combina con
# un vector de inicializaion que llamaremos nonce, además de utilizar la llave tradicional.
# El texto cifrado devuelve el IV, el texto cifrado y una etiqueta de auténticación.

# ii. ¿Qué parámetros tuvo que hacer llegar desde su función de Encrypt a la Decrypt? ¿Por qué?
# La función encrypt nos devuelve los parametros de una clave IV de inicialización, nuestra llave proporcionada
# por el usuario, el texto cifrado y una etiqueta opcional de auténticación.
# A decrypt hacemos llegar la IV, la clave del usuario y el texto cifrado, esto porque es necesario
# tener la clave del usuario y la IV, para generar todas las llaves para el proceso de descifrado y que este sea correcto.
# La etiqueta de auténticación únicamente es necesaria si finalmente se desea auténticar, el devolver cualquier mensaje 
# al usuario del programa. Sin embargo, sin la clave correcta e IV no podrá obtener el mensaje.

# iii. ¿Qué variables considera las más importantes dentro de su implementación? ¿Por qué?
# Las variables más importantes dentro de nuestra implementación son el password que es la llave del AES,
# el nonce que es la IV del AES y tanto las variables plaintext como ciphertext que representan nuestros textos planos y cifrados.
# De igual forma, tienen gran importancia nuestros ciphers que creamos a partir de las variables anteriores, y que finalmente
# nos permiten interactuar con un modo de AES y encriptados/descifrados.
# Por último, tenemos varias variables de archivos que son los que leemos y escribimos para interactuar con los usuarios.

# Importamos la libreria que utilizaremos de AES
from Crypto.Cipher import AES




#Iniciamos nuestro programa con un menu para encriptar archivos o desencriptar archivos con el password y nonce para el aes
menu="""
Bienvenido al sistema de encriptado y desencriptado de 
archivos utilizando AES. El menú es el siguiente:
    1. Ingrese la opción 1 para encriptar un archivo.
    2. Ingresa la opción 2 para descencriptar un archivo.
    3. Ingrese cualquier otra cosa para salir.
Ingrese su opción: 
"""

option="1"
while option=="1" or option=="2":
    #Imprimimos menu
    option=input(menu)

    #Si desea encriptar
    if(option=="1"):  
        #Pedimos archivo para encriptar su contenido  
        file=input("Ingrese el nombre del archivo para encriptar con su extensión: ")
        # try:
        try:
            fileLines = open('./aesFile/'+file, "r").read()
            plainText= fileLines.encode('latin-1')
            while True:
                #Pedimos la contraseña y vericamos que cumpla con la longitudad
                key = input('Ingrese la contraseña a utilizar: ')
                if(len(key)==16):
                    bKey = str.encode(key)
                    break
                else:
                    print('Error. La contraseña debe tener 16 caracteres')
        
            #Comenzamos con el encriptado mode GCM
            cipher = AES.new(bKey, AES.MODE_GCM)
            #Obtenemos IV que llamaremos nonce y será necesaria darsela al usuario con su texto cifrado
            nonce = cipher.nonce
            #Ciframos el texto plano
            ciphertext, tag = cipher.encrypt_and_digest(plainText)
            print("Su archivo ha sido cifrado. El archivo resultante fue escrito en encrypted.txt.\nSu contraseña fue escrita en password.txt. \nSu clave nonce fue escrita en nonce.txt")
            #Escribimos los resultados al usuario en archivos
            #encrypted.txt contenido encriptado
            #password.txt contraseña
            #nonce.txt IV
            cipherfile = open('./aesFile/'+"encrypted.txt", "w",encoding="latin-1")
            cipherfile.write(ciphertext.decode('latin-1'))
            cipherfile.close()
            cipherfile = open('./aesFile/'+"password.txt", "w",encoding="latin-1")
            cipherfile.write(bKey.decode('latin-1'))
            cipherfile.close()
            cipherfile = open('./aesFile/'+"nonce.txt", "w",encoding="latin-1")
            cipherfile.write(nonce.decode('latin-1'))
            cipherfile.close()

        except FileNotFoundError:
            #Si hay error en el archivo
            print("Error, ingrese un archivo válido.")

    #Si desea desencriptar
    elif(option=="2"):
        #Pedimos los archivos necesarios el encriptado,contraseña y nonce.
        fileDecrypt=input("Ingrese el nombre del archivo para desencriptar con su extensión: ")
        filePassword=input("Ingrese el nombre del archivo con la contraseña: ")
        fileNonce=input("Ingrese el nombre del archivo con el nonce: ")
        try:
            #Convertimos a bytes los contenidos
            ciphertext = open(fileDecrypt, "r",encoding="latin-1").read().encode('latin-1') 
            bKey = open(filePassword, "r",encoding="latin-1").read().encode('latin-1') 
            nonce = open(fileNonce, "r",encoding="latin-1").read().encode('latin-1') 
            #Comenzamos los desencriptados
            cipher = AES.new(bKey, AES.MODE_GCM,nonce)
            decrypted=str(cipher.decrypt(ciphertext).decode('latin-1'))
            #Escribimos el mensaje desencriptado en decrypted.txt
            print("Su mensaje desencriptado es el siguiente: \n" ,decrypted)
            print("Ha sido escrito en el archivo decrypted.txt")
            cipherfile = open('./aesFile/'+"decrypted.txt", "w",encoding="latin-1")
            cipherfile.write(decrypted)
            cipherfile.close()
        except FileNotFoundError:
            #Si hubiese error, en los archivos
            print("Error, debe ingresar archivos válido.")  
        except:
            #Cualquier otra error al desencriptar es problema de los datos dados.
            print("Error, en los datos proporcionados para desencriptar.")

print("Gracias por utilizar nuestro programa.")
