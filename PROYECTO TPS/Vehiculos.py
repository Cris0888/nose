# Importamos las librerias

from flask import redirect, render_template
from datetime import datetime
import os

class Vehiculos:
    def __init__(self,prog,conDB,cursor):
        self.prog = prog
        self.conDB = conDB 
        self.cursor=cursor

    def agregar(self,auto):
        sql=f"INSERT INTO gest_vehic (id_placa,marca,num_ocupa,estado,consumo,soat,tecno_mec,permiso_cir,kilometraje,img,precio) VALUES ('{auto[0]}','{auto[1]}','{auto[2]}',{auto[3]},'{auto[4]}','{auto[5]}','{auto[6]}','{auto[7]}',{auto[8]},'{auto[9]}',{auto[10]})"
        self.cursor.execute(sql)
        self.conDB.commit()
    
    def buscar(self,placa):
        sql=f"SELECT * FROM gest_vehic WHERE id_placa ='{placa}'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    
    def consultar(self):
        sql = "SELECT * FROM gest_vehic"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        return resultado
    
    def modifica(self,placa):
        sql=f"UPDATE gest_vehic SET marca='{placa[1]}',num_ocupa='{placa[2]}',estado={placa[3]},consumo='{placa[4]}',soat='{placa[5]}',tecno_mec='{placa[6]}',permiso_cir='{placa[7]}',kilometraje={placa[8]},img='{placa[9]}',precio={placa[10]} WHERE id_placa='{placa[0]}'"
        self.cursor.execute(sql)
        self.conDB.commit()

    def borrar(self,placa):
        sql =f"DELETE FROM gest_vehic WHERE id_placa ='{placa}'"
        self.cursor.execute(sql)
        self.conDB.commit()
        