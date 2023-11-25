import hashlib

class Usuarios:
    def __init__(self,prog,conDB,cursor):
        self.prog = prog
        self.conDB = conDB
        self.cursor = cursor
    
    def loguear(self,id,contra):
        cifrada = hashlib.sha512(contra.encode("utf-8")).hexdigest()
        sql=f"SELECT usuario FROM login WHERE usuario='{id}' AND password='{cifrada}'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado

    def buscar(self,id):
        sql = f"SELECT * FROM login WHERE usuario='{id}'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.conexion.commit()
        return resultado
    
    def agregar(self,usuario):
        cifrada=hashlib.sha512(usuario[2].encode("utf-8")).hexdigest()
        sql=f"INSERT INTO login (usuario,password) VALUES ('{usuario[0]}','{usuario[1]}')"
        self.cursor.execute(sql)
        self.conDB.commit()
