import hashlib

contrasena = input("Digite contraseña: ")
cifrada = hashlib.sha512(contrasena.encode("utf-8")).hexdigest()
print(cifrada)