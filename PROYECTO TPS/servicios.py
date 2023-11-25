# Importamos las librerias

from flask import redirect, render_template
from datetime import datetime
import os

# Creamos la clase y definimos las funciones CRUD

class Servicios:
    def __init__(self,prog,conDB,cursor):
        self.prog = prog
        self.conDB = conDB
        self.cursor = cursor

# Funcion agregar

    def agregar(self,serv):    
        ahora = datetime.now()
        fname,fext = os.path.splitext(serv[7].filename)
        nombreFoto= "E"+ahora.strftime("%Y%m%d%H%M%S")+fext
        serv[7].save("uploads/"+nombreFoto)
        sql = f"INSERT INTO servicios (idServicio,nombre,descripcion,duracion,precio,iva,estado,foto) VALUES ({serv[0]},'{serv[1]}','{serv[2]}',{serv[3]},{serv[4]},'{serv[5]}','{serv[6]}','{nombreFoto}')"
        self.cursor.execute(sql)
        self.conDB.commit()
        
# Funcion buscar
        
    def buscar(self,num):
        sql=f"SELECT * FROM servicios WHERE idServicio={num}"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    
# Funcion consultar

    def consultar(self):
        sql = "SELECT * FROM servicios WHERE borrado=0"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        return resultado

# Funcion actualizar
    
    def actualiza(self,serv):
        sql=f"UPDATE servicios SET nombre='{serv[1]}', descripcion='{serv[2]}',duracion='{serv[3]}',\
        precio={serv[4]},iva={serv[5]},estado='{serv[6]}'\
        WHERE idServicio={serv[0]}"
        self.cursor.execute(sql)
        self.conDB.commit()
        if serv[7].filename != "":
            sql=f"SELECT foto FROM servicios WHERE idServicio={serv[0]}"
            self.cursor.execute(sql)
            resultado = self.cursor.fetchall()
            self.conDB.commit()
            os.remove(os.path.join(self.prog.config['CARPETAUP'],resultado[0][0]))
            ahora = datetime.now()
            fname,fext = os.path.splitext(serv[7].filename)
            nombreFoto= "E"+ahora.strftime("%Y%m%d%H%M%S")+fext
            serv[7].save("uploads/"+nombreFoto)
            sql = f"UPDATE servicios SET foto='{nombreFoto}' WHERE idServicio={serv[0]}"
            self.cursor.execute(sql)
            self.conDB.commit()
    
    # Funcion borrar
            
    def borrar(self,id):
        sql = f"UPDATE servicios SET borrado=1 WHERE idServicio={id}"
        self.cursor.execute(sql)
        self.conDB.commit()
