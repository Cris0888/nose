# Importamos las librerias

from flask import redirect, render_template
from datetime import datetime
import os

# Creamos la clase y definimos las funciones CRUD


class Comandas:
    def __init__(self, prog, conDB, cursor):
        self.prog = prog
        self.conDB = conDB
        self.cursor = cursor


# Funcion agregar

    def agregar(self,com):
        ahora = datetime.now()
        fname, fext = os.path.splitext(com[10].filename)
        nombreFoto = "E"+ahora.strftime("%Y%m%d%H%M%S")+fext
        com[10].save("uploads/"+nombreFoto)
        sql = f"INSERT INTO comandas (idcomanda,idcodigo,descripItem,idRegistro,idHabitacion,fecha,cantidad,\
            valor,subtotal,estado,foto) VALUES ({com[0]},'{com[1]}',{com[2]},{com[3]},{com[4]},'{com[5]}', '{com[6]}','{com[7]}','{com[8]}','{com[9]}','{nombreFoto}')"
        self.cursor.execute(sql)
        self.conDB.commit()

# Funcion buscar

    def buscar(self,num):
        sql = f"SELECT * FROM comandas WHERE idcomanda={num}"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado

# Funcion consultar

    def consultar(self):
        sql = "SELECT * FROM comandas WHERE borrado=0"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        return resultado

# Funcion actualizar

    def actualiza(self,com):
        sql = f"UPDATE comandas SET idcodigo='{com[1]}', descripItem={com[2]}, idRegistro={com[3]},\
           idHabitacion='{com[4]}', fecha='{com[5]}', cantidad='{com[6]}',valor='{com[7]}',subtotal='{com[8]}\',estado='{com[9]}' WHERE idcomanda={com[0]}"
        self.cursor.execute(sql)
        self.conDB.commit()
        if com[10].filename != "":
            sql=f"SELECT foto FROM comandas WHERE idcomanda={com[0]}"
            self.cursor.execute(sql)
            resultado = self.cursor.fetchall()
            self.conDB.commit()
            os.remove(os.path.join(self.prog.config['CARPETAUP'],resultado[0][0]))
            ahora = datetime.now()
            fname,fext = os.path.splitext(com[10].filename)
            nombreFoto= "E"+ahora.strftime("%Y%m%d%H%M%S")+fext
            com[10].save("uploads/"+nombreFoto)
            sql = f"UPDATE comandas SET foto='{nombreFoto}' WHERE idcomanda={com[0]}"
            self.cursor.execute(sql)
            self.conDB.commit()

    # Funcion borrar

    def borrar(self, id):
        sql = f"UPDATE comandas SET borrado=1 WHERE idcomanda={id}"
        self.cursor.execute(sql)
        self.conDB.commit()
