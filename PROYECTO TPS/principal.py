from datetime import datetime, timedelta
import hashlib
from random import randint
from flask import Flask,redirect,render_template,request,send_from_directory,session
import mysql.connector
import os

from usuarios import Usuarios
from Vehiculos import Vehiculos
from productos import Productos
from servicios import Servicios
from comandas import Comandas
from facturas import Facturas


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
misUsuarios = Usuarios(prog,conexion,miCursor)
misVehiculos = Vehiculos(prog, conexion, miCursor)
misProductos = Productos(prog,conexion,miCursor)
misServicios = Servicios(prog,conexion,miCursor)
misFacturas = Facturas(prog,conexion,miCursor)
misComandas = Comandas(prog,conexion,miCursor)

CARPETAUP = os.path.join('uploads')
prog.config['CARPETAUP'] = CARPETAUP

@prog.route('/uploads/<nombre>')
def uploads(nombre):
    return send_from_directory(prog.config['CARPETAUP'],nombre)

# Ruta para  Usuarios ( Grupo Aidalia )

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
        return render_template("login.html",msg="Credenciales incorrectas")
    
# Establecemos la ruta a templates/principal


@prog.route('/principal')
def principal():
    if session.get('loginOk'):
        return render_template("principal.html")
    else:
        return redirect('/')

   
# Ruta para Vehiculos ( Grupo Harold David )

@prog.route('/Catalogo')
def catalogo():
    sql = "SELECT * FROM gest_vehic"
    miCursor.execute(sql)
    resultado = miCursor.fetchall()
    return render_template("Vehiculos/catalogo.html", res=resultado)

@prog.route('/Alquiler')
def alquiler():
    return render_template("Vehiculos/Alquiler.html", msg="")

@prog.route('/Devolucion')
def devolucion():
    return render_template("Vehiculos/devolucion.html", msg="")


@prog.route("/Borrarauto/<placa>")
def Borrar(placa):
    misVehiculos.borrar(placa)
    return redirect ('/Catalogo')

@prog.route('/agregarauto')
def agregar():
    return render_template("Vehiculos/agregar.html")

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
        return render_template("Vehiculos/agregar.html",msg="Vehiculo existente")
    else:
        misVehiculos.agregar(auto)
        return redirect ("Catalogo")
    
@prog.route('/modificaproducto/<placa>')
def modifica(placa):
    resultado=misVehiculos.buscar(placa)
    return render_template("Vehiculos/modificarauto.html", placa=resultado[0])

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
    return redirect('Catalogo')

# Ruta para Productos ( Grupo Adriana Herrera )

@prog.route('/productos')
def productos():
    if session.get('loginOk'):
        resultado = misProductos.consultar()
        return render_template("productos/productos.html",res=resultado)
    else:
        return redirect('/')

@prog.route('/agregaproducto')
def agregaproducto():
    if session.get('loginOk'): 
        return render_template("productos/agregaproducto.html", mensaje="")
    

@prog.route("/guardaproducto", methods=['POST'])
def guardaproducto():
    num = request.form['numero']
    nomp = request.form['nomProd']
    desc = request.form['descripcion']
    cant = request.form['cantidad']
    prec = request.form['precio']
    iv = request.form['iva']
    est = request.form['estado']
    fot = request.files['foto']
    producto=[num,nomp,desc,cant,prec,iv,est,fot]
    if len(misProductos.buscar(num))>0:
        return render_template("productos/agregaproducto.html",mensaje="Número de producto ya existe!!!")
    else:
        misProductos.agregar(producto)
        return redirect('/productos')

@prog.route("/modificarproducto/<num>")
def modificarproducto(num):
    if session.get('loginOk'):
        resultado = misProductos.buscar(num)
        return render_template("productos/modificarproducto.html",prod=resultado[0])
    else:
        return redirect('/')

@prog.route("/actualizaproducto", methods=['POST'])
def actualizaproducto():
    num = request.form['numero']
    nomp = request.form['nomProd']
    desc = request.form['descripcion']
    cant = request.form['cantidad']
    prec = request.form['precio']
    iv = request.form['iva']
    est = request.form['estado']
    fot = request.files['foto']
    producto=[num,nomp,desc,cant,prec,iv,est,fot]
    misProductos.actualiza(producto)
    return redirect("/productos")

@prog.route("/borraproducto/<id>")
def borraproducto(id):
    if session.get('loginOk'):
        misProductos.borrar(id)
        return redirect("/productos")
    else:
        return redirect('/')
 
# Ruta para Servicios ( Grupo Adriana Herrera )

@prog.route('/servicios')
def servicios():
    if session.get('loginOk'):
        resultado = misServicios.consultar()
        return render_template("servicios/servicios.html",res=resultado)
    else:
        return redirect('/')

@prog.route('/agregaservicio')
def agregaservicio():
    if session.get('loginOk'): 
        return render_template("servicios/agregaservicio.html", mensaje="")
     

@prog.route("/guardaservicio", methods=['POST'])
def guardaservicio():
    num = request.form['numero']
    noms = request.form['nomServ']
    desc = request.form['descripcion']
    dur = request.form['duracion']
    prec = request.form['precio']
    iv = request.form['iva']
    est = request.form['estado']
    fot = request.files['foto']
    servicio=[num,noms,desc,dur,prec,iv,est,fot]
    if len(misServicios.buscar(num))>0:
        return render_template("servicios/agregaservicio.html",mensaje="Número de servicio ya existe!!!")
    else:
        misServicios.agregar(servicio)
        return redirect('/servicios')

@prog.route("/modificaservicio/<num>")
def modificaservicio(num):
    if session.get('loginOk'):
        resultado = misServicios.buscar(num)
        return render_template("servicios/modificaservicio.html",serv=resultado[0])
    else:
        return redirect('/')

@prog.route("/actualizaservicio", methods=['POST'])
def actualizaservicio():
    num = request.form['numero']
    noms = request.form['nomServ']
    desc = request.form['descripcion']
    dur = request.form['duracion']
    prec = request.form['precio']
    iv = request.form['iva']
    est = request.form['estado']
    fot = request.files['foto']
    servicio=[num,noms,desc,dur,prec,iv,est,fot]
    misServicios.actualiza(servicio)
    return redirect("/servicios")

@prog.route("/borraservicio/<id>")
def borraservicio(id):
    if session.get('loginOk'):
        misServicios.borrar(id)
        return redirect("/servicios")
    else:
        return redirect('/') 
 
# Ruta para Facturas ( Grupo Adriana Herrera )

@prog.route('/facturas')
def facturas():
    if session.get('loginOk'):
        resultado = misFacturas.consultar()
        return render_template("facturas/facturas.html",res=resultado)
    else:
        return redirect('/')

@prog.route('/agregafactura')
def agregafactura():
    if session.get('loginOk'): 
        return render_template("facturas/agregafactura.html", mensaje="")
     

@prog.route("/guardafactura", methods=['POST'])
def guardafactura():
    num = request.form['numero']
    nomr = request.form['idRegistro']
    clie = request.form['idCliente']
    coma = request.form['idcomanda']
    fec = request.form['fecha']
    tot = request.form['total']
    factura=[num,nomr,clie,coma,fec,tot]
    if len(misFacturas.buscar(num))>0:
        return render_template("facturas/agregafactura.html",mensaje="Número de factura ya existe!!!")
    else:
        misFacturas.agregar(factura)
        return redirect('/facturas')

@prog.route("/modificafactura/<num>")
def modificafactura(num):
    if session.get('loginOk'):
        resultado = misFacturas.buscar(num)
        return render_template("facturas/modificafactura.html",fact=resultado[0])
    else:
        return redirect('/')

@prog.route("/actualizafactura", methods=['POST'])
def actualizafactura():
    num = request.form['numero']
    nomr = request.form['idRegistro']
    clie = request.form['idCliente']
    coma = request.form['idcomanda']
    fec = request.form['fecha']
    tot = request.form['total']
    factura=[num,nomr,clie,coma,fec,tot]
    misFacturas.actualiza(factura)
    return redirect("/facturas")

@prog.route("/borrafactura/<id>")
def borrafactura(id):
    if session.get('loginOk'):
        misFacturas.borrar(id)
        return redirect("/facturas")
    else:
        return redirect('/') 

# Ruta para Comandas ( Grupo Adriana Herrera )


@prog.route('/comandas')
def comandas():
    if session.get('loginOk'):
       resultado = misComandas.consultar()
       return render_template("comandas/comandas.html", res=resultado)
    else:
        return redirect('/')


@prog.route('/agregacomanda')
def agregacomanda():
    if session.get('loginOk'):
        return render_template("comandas/agregacomanda.html", mensaje="")



@prog.route("/guardacomanda", methods=['POST'])
def guardacomanda():

    num = request.form['numero']
    idcod = request.form['idcodigo']
    desc = request.form['descripItem']
    reg = request.form['idRegistro']
    hab = request.form['idHabitacion']
    fech = request.form['fecha']
    cant = request.form['cantidad']
    val = request.form['valor']
    sub = request.form['subtotal']
    est = request.form['estado']
    fot = request.files['foto']
    comanda = [num, idcod, desc, reg, hab, fech, cant, val, sub, est, fot]
    if len(misComandas.buscar(num)) > 0:
        return render_template("comandas/agregacomanda.html", mensaje="Número de comanda ya existe!!!")
    else:
        misComandas.agregar(comanda)
        return redirect('/comandas')


@prog.route("/modificacomanda/<num>")
def modificacomanda(num):
    if session.get('loginOk'):
        resultado = misComandas.buscar(num)
        return render_template("comandas/modificacomanda.html", com=resultado[0])
    else:
        return redirect('/')


@prog.route("/actualizacomanda", methods=['POST'])
def actualizacomanda():
    num = request.form['numero']
    idcod = request.form['idcodigo']
    desc = request.form['descripItem']
    reg = request.form['idRegistro']
    hab = request.form['idHabitacion']
    fech = request.form['fecha']
    cant = request.form['cantidad']
    val = request.form['valor']
    sub = request.form['subtotal']
    est = request.form['estado']
    fot = request.files['foto']
    comanda = [num, idcod, desc, reg, hab, fech, cant, val, sub, est, fot]
    misComandas.actualiza(comanda)
    return redirect("/comandas")


@prog.route("/borracomanda/<id>")
def borracomanda(id):
    if session.get('loginOk'):
        misComandas.borrar(id)
        return redirect("/comandas")
    else:
        return redirect('/')

    
# Este codigo hace parte de la libreria de Flask para crear el servidor local    
    
if __name__ == '__main__':
    prog.run(host='0.0.0.0',debug=True,port='8085')