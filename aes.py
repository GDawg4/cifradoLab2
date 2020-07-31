from Crypto.Cipher import AES

mensaje = """
¿Qué desea hacer?
1. Encriptar mensaje
2. Desencriptar mensaje
3. Salir
"""

#Tuvimos que guardar el texto encriptado para poder procesarlo la segunda vez
#La contraseña debe ser ingresada nuevamente y no hay más variables en este sistema

selectedOption = ''
ciphertext = ''

while True:
    print(mensaje)
    selectedOption = input('\n')

    if selectedOption == '1':
        #Tuvimos que usar encode en las variables que ingresa el usuario
        #Eso incluye el texto a encriptar y las contraseñas utilizadas
        data = input('Ingrese el texto a desencriptar \n')
        bData = str.encode(data)
        key = input('Ingrese la contraseña a utilizar \n')
        bKey = str.encode(key)
        try:
            #Se utilizó el modo EAX
            #Se utilizó este modo, ya que permite procesar mensajes de largo arbitrario
            cipher = AES.new(bKey, AES.MODE_EAX)
            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(bData)
        except ValueError:
            print('La clave debe tener 16 caracteres')

    elif selectedOption == '2':
        key = input('Ingrese la contraseña a utilizar \n')

        try:
            bKey = str.encode(key)
            cipher = AES.new(bKey, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)
        except ValueError:
            print('La clave debe tener 16 caracteres')
            
        try:
            cipher.verify(tag)
            print("The message is authentic:", plaintext)
        except ValueError:
            print("Key incorrect or message corrupted")
    elif selectedOption == '3':
        break
print('Gracias por usar nuestro sistema')
