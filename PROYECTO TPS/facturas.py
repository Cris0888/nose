# Importamos las librerias

from flask import redirect, render_template
from datetime import datetime
import os

# Creamos la clase y definimos las funciones CRUD

class Facturas:
    def __init__(self,prog,conDB,cursor):
        self.prog = prog
        self.conDB = conDB
        self.cursor = cursor

# Funcion agregar

    def agregar(self,fact):    
        sql = f"INSERT INTO facturas (idfactura,idRegistro,idCliente,fecha,total) VALUES ({fact[0]},{fact[1]},'{fact[2]}',{fact[3]},{fact[4]},{fact[5]})"
        self.cursor.execute(sql)
        self.conDB.commit()
        
# Funcion buscar
        
    def buscar(self,num):
        sql=f"SELECT * FROM facturas WHERE idfactura={num}"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    
# Funcion consultar

    def consultar(self):
        sql = "SELECT * FROM facturas WHERE borrado=0"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        return resultado

# Funcion actualizar
    
    def actualiza(self,fact):
        sql = f"UPDATE facturas SET idRegistro='{fact[1]}', idCliente='{fact[2]}',idcomanda='{fact[3]}', fecha='{fact[4]}',total='{fact[5]}' WHERE idfactura={fact[0]}"
        self.cursor.execute(sql)
        self.conDB.commit()
    
    # Funcion borrar
            
    def borrar(self,id):
        sql = f"UPDATE facturas SET borrado=1 WHERE idfactura={id}"
        self.cursor.execute(sql)
        self.conDB.commit()
