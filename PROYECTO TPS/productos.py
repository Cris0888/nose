# Importamos las librerias

from flask import redirect, render_template
from datetime import datetime
import os

# Creamos la clase y definimos las funciones CRUD

class Productos:
    def __init__(self,prog,conDB,cursor):
        self.prog = prog
        self.conDB = conDB
        self.cursor = cursor

# Funcion agregar

    def agregar(self,prod):    
        ahora = datetime.now()
        fname,fext = os.path.splitext(prod[7].filename)
        nombreFoto= "E"+ahora.strftime("%Y%m%d%H%M%S")+fext
        prod[7].save("uploads/"+nombreFoto)
        sql = f"INSERT INTO productos (idProd,nombre,descripcion,cantidad,\
            precio,estado,foto) VALUES ({prod[0]},'{prod[1]}',\
            '{prod[2]}',{prod[3]},{prod[4]},'{prod[5]}','{nombreFoto}')"
        self.cursor.execute(sql)
        self.conDB.commit()
        
# Funcion buscar
        
    def buscar(self,num):
        sql=f"SELECT * FROM productos WHERE idProd={num}"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    
# Funcion consultar

    def consultar(self):
        sql = "SELECT * FROM productos WHERE borrado=0"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        return resultado

# Funcion actualizar
    
    def actualiza(self,prod):
        sql=f"UPDATE productos SET nombre='{prod[1]}', descripcion='{prod[2]}',cantidad='{prod[3]}',\
        precio={prod[4]}, iva='{prod[5]}',estado='{prod[6]}' WHERE idProd={prod[0]}"
        self.cursor.execute(sql)
        self.conDB.commit()
        if prod[7].filename != "":
            sql=f"SELECT foto FROM productos WHERE idProd={prod[0]}"
            self.cursor.execute(sql)
            resultado = self.cursor.fetchall()
            self.conDB.commit()
            os.remove(os.path.join(self.prog.config['CARPETAUP'],resultado[0][0]))
            ahora = datetime.now()
            fname,fext = os.path.splitext(prod[7].filename)
            nombreFoto= "E"+ahora.strftime("%Y%m%d%H%M%S")+fext
            prod[7].save("uploads/"+nombreFoto)
            sql = f"UPDATE productos SET foto='{nombreFoto}' WHERE idProd={prod[0]}"
            self.cursor.execute(sql)
            self.conDB.commit()
    
    # Funcion borrar
            
    def borrar(self,id):
        sql = f"UPDATE productos SET borrado=1 WHERE idProd={id}"
        self.cursor.execute(sql)
        self.conDB.commit()
