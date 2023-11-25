from datetime import datetime, timedelta
import hashlib
from random import randint
from flask import Flask,redirect,render_template,request,send_from_directory,session
import mysql.connector
import os

from usuarios import Usuarios
from Vehiculos import Vehiculos

prog = Flask(__name__)
prog.secret_key=str(randint(100000,999999))
prog.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test",
)
miCursor = conexion.cursor()
misVehiculos= Vehiculos(prog,conexion,miCursor)
misUsuarios = Usuarios(prog,conexion,miCursor)

CARPETAUP = os.path.join('uploads')
prog.config['CARPETAUP'] = CARPETAUP

@prog.route('/uploads/<nombre>')
def uploads(nombre):
    return send_from_directory(prog.config['CARPETAUP'],nombre)

@prog.route('/')
def index():
    return render_template("usuarios/login.html",msg="")

@prog.route('/login',methods=['POST'])
def login():
    id = request.form['uname']
    contra = request.form['psw']
    resultado = misUsuarios.loguear(id,contra)
    if len(resultado)>0:
        session['loginOk'] = True
        session['nomUsuario'] = resultado[0][0]
        #session['rol'] = resultado[0][1]
        return render_template("principal.html",nom=resultado[0][0])
    else:
        return render_template("usuarios/login.html",msg="Credenciales incorrectas")
    

@prog.route('/Catalogo')
def catalogo():
    sql = "SELECT * FROM gest_vehic"
    miCursor.execute(sql)
    resultado = miCursor.fetchall()
    return render_template("catalogo.html", res=resultado)

@prog.route('/Alquiler')
def alquiler():
    return render_template("Alquiler.html", msg="")

@prog.route('/Devolucion')
def devolucion():
    return render_template("devolucion.html", msg="")


@prog.route("/Borrarauto/<placa>")
def Borrar(placa):
    misVehiculos.borrar(placa)
    return redirect ('/Catalogo')

@prog.route('/agregarauto')
def agregar():
    return render_template("agregar.html")

@prog.route('/agregar',methods=['POST'])
def agregarGuardar():
    plac=request.form['Placa']
    marc=request.form['Marca']
    numOcup=request.form['numOcupantes']
    estd=request.form['estado']
    consum=request.form['consumo']
    soat=request.form['soat']
    tecnoMec=request.form['tecno_mec']
    perm=request.form['permiso']
    kilom=request.form['kilometraje']
    img=request.form['img']
    prec=request.form['precio']
    auto=[plac,marc,numOcup,estd,consum,soat,tecnoMec,perm,kilom,img,prec]
    if len(misVehiculos.buscar(plac))>0:
        return render_template("agregar.html",msg="Vehiculo existente")
    else:
        misVehiculos.agregar(auto)
        return redirect ("/Catalogo")
    
@prog.route('/modificaproducto/<placa>')
def modifica(placa):
    resultado=misVehiculos.buscar(placa)
    return render_template("modificarauto.html",placa=resultado[0])

@prog.route('/modificarGuardar',methods=['POST'])
def modificaGuardar():
    plac=request.form['Placa']
    marc=request.form['Marca']
    numOcup=request.form['numOcupantes']
    estd=request.form['estado']
    consum=request.form['consumo']
    soat=request.form['soat']
    tecnoMec=request.form['tecno_mec']
    perm=request.form['permiso']
    kilom=request.form['kilometraje']
    img=request.form['img']
    prec=request.form['precio']
    auto=[plac,marc,numOcup,estd,consum,soat,tecnoMec,perm,kilom,img,prec]
    misVehiculos.modifica(auto)
    return redirect('/Catalogo')

    
if __name__ == '__main__':
    prog.run(host='0.0.0.0',debug=True,port='8085')