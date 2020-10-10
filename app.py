from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS, cross_origin
import os
from flask_sqlalchemy import SQLAlchemy
from orm import Numeros, Usuarios, Numerosv, Usuariosv, Pago, Pagov
from datetime import datetime, date
import time
from datetime import datetime, timedelta
import requests
from flask_mail import Mail,  Message
from flask_api import FlaskAPI
#from flask.ext.api import FlaskAPI

app = FlaskAPI(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@localhost:3306/landroid"
app.config['SECRET_KEY'] = 'T1BJXrQJa2eoUf0pA/gu19CbdS0uM='
#api = Api(app)
db = SQLAlchemy(app)
#app.config['CORS_HEADERS'] = 'Content-Type'
#CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'chancemilliondayvincicasa@gmail.com',
    MAIL_PASSWORD = 'ABchance2020',
))
mail = Mail(app)

@app.route('/registro', methods = ['POST'])
def registro():
	datos = request.get_json()
	validar = db.session.query(Usuarios.correo).filter_by(correo = datos['correo']).scalar() is not None
	if validar == None:
		usuario = Usuarios(nombre = datos['nombre'], correo = datos['correo'], fechan = datos['fecha'], password = datos['password'], sexo = datos['sexo'])
		db.session.add(usuario)
		db.session.commit()
		session['correo'] = datos['correo']
		return jsonify(respuesta = 'Usuario registrado satisfactoriamente')
	else:
		return jsonify(respuesta = 'registrado')

@app.route('/sesion', methods = ['POST'])
def sesion():
	datos = request.get_json()
	validar = db.session.query(Usuarios.correo).filter_by(correo = datos['correo']).scalar() is not None
	if validar == None or validar == False:
		return jsonify(respuesta = 'nousuario')
	else:
		validar2 = db.session.query(Usuarios).filter(Usuarios.correo == datos['correo']).first()
		session['correo'] = datos['correo']

		return jsonify(respuesta = str(validar2.password), nombre = str(validar2.nombre), correo = str(validar2.correo), fechan = str(validar2.fechan), sexo = str(validar2.sexo));

		# return validar2
		# for resultado in validar2:
			# return jsonify(respuesta = str(resultado.password), nombre = str(resultado.nombre))
			# return jsonify(respuesta = str(resultado.password), user = str(resultado.nombre))

@app.route('/usuarios', methods = ['GET'])
def usuarios():
	usuarios = db.session.query(Usuarios).all() #.filter(Usuarios.correo == datos['correo']).first()
	new_usuarios = []

	for x in usuarios:
		new_usuarios.append({"nombre":x.nombre,"correo":x.correo, "fechan":x.fechan, "sexo":x.sexo});

	return jsonify(usuarios = new_usuarios)

@app.route('/winners', methods = ['GET'])
def winners():
    ganadores = db.session.query(Numeros).all()
    new_ganadores = []
    for x in ganadores:
        new_ganadores.append({"numero":x.numero,"usuario":x.usuario, "fjugada":x.fjugada, "aciertos":x.aciertos})
        return jsonify(ganadores = new_ganadores)

@app.route('/numeros', methods = ['POST'])
def numeros():
	datos = request.get_json()
	now = datetime.now()
	fecha = now.date()
	numero = Numeros(numero = datos['numero'], usuario = datos['correo'], fjugada = fecha, aciertos = datos['puntos'])
	db.session.add(numero)
	db.session.commit()
	return jsonify(respuesta = 'Número registrado satisfactoriamente')

@app.route('/scrapper3', methods = ['GET'])
def scrapping3():
    fecha = datetime.now().strftime('%Y%m%d')
    r = requests.post('https://www.lottomaticaitalia.it/md/estrazioni-e-vincite/ultime-estrazioni-millionDay.json', json = {'numeroEstrazioni': '200', 'data': fecha}, headers = {'Content-Type': 'application/json'})
    f = requests.get('https://www.lottomaticaitalia.it/md/statistiche-million-day/numeri-frequenti.json')
    ri = requests.get('https://www.lottomaticaitalia.it/md/statistiche-million-day/numeri-ritardatari.json')
    ganadores = requests.get('http://m.vincicasa.it/sisal-gn-proxy-servlet-web/proxy/gntn-info-web/rest/gioco/vincicasa/estrazioni/ultimoconcorso')
    # return ganadores.text
    return jsonify(r.text, f.text, ri.text, ganadores.text)

@app.route('/recuperar', methods = ['POST'])
def recuperar():
	datos = request.get_json()
	correo = datos['correo']
	msg = Message("", sender = "chancemilliondayvincicasa@gmail.com", recipients = [correo])
	msg.html = '<a href="http://axelrace.pythonanywhere.com/password">Clicca qui per recuperare la tua password</a>'
	mail.send(msg)
	return jsonify('Mensaje enviado exitosamente')

@app.route('/password')
def password():
    return render_template('recuperar.html')

@app.route('/cambio', methods = ['POST'])
def cambio():
	datos = request.get_json()
	validar = db.session.query(Usuarios.correo).filter_by(correo = datos['correo']).scalar() is not None
	if validar == None or validar == False:
		return jsonify(respuesta = 'nousuario')
	else:
		db.session.query(Usuarios).filter(Usuarios.correo == datos['correo']).update(dict(password = datos['password']))
		db.session.commit()
		return jsonify('Cambio realizado exitosamente')

@app.route('/ganador', methods = ['POST'])
def ganador():
	datos = request.get_json()
	msg = Message("L'utente " + datos["usuario"] + " ha vinto con " + datos["puntos"] + " punti", sender = "chancemilliondayvincicasa@gmail.com", recipients = ['chancemilliondayvincicasa@gmail.com'])
	mail.send(msg)
	msg = Message("Congratulazioni! hai vinto alla lotteria con " + datos["puntos"] + " punti", sender = "chancemilliondayvincicasa@gmail.com", recipients = [datos["correo"]])
	mail.send(msg)
	return jsonify('Mensajes enviados exitosamente')

@app.route('/pago', methods = ['GET', 'POST'])
def pago():
    if request.method == 'POST':
    	datos = request.get_json()
    	now = datetime.now()
    	fecha = now.date()
    	pago = Pago(usuario = datos['usuario'], correo = datos['correo'], fecha = fecha, monto = datos['monto'])
    	db.session.add(pago)
    	db.session.commit()
    	return jsonify('Pago registrado')
    else:
        donadores = db.session.query(Pago).all()
        new_donadores = []
        for x in donadores:
            new_donadores.append({"correo":x.correo,"usuario":x.usuario, "fecha":x.fecha, "monto":x.monto})
        return jsonify(donadores = new_donadores)

@app.route('/registrov', methods = ['POST'])
def registrov():
	datos = request.get_json()
	validar = db.session.query(Usuariosv.correo).filter_by(correo = datos['correo']).scalar() is not None
	if validar != None:
		usuario = Usuariosv(nombre = datos['nombre'], correo = datos['correo'], fechan = datos['fecha'], password = datos['password'], sexo = datos['sexo'])
		db.session.add(usuario)
		db.session.commit()
		session['correo'] = datos['correo']
		return jsonify(respuesta = 'Usuario registrado satisfactoriamente')
	else:
		return jsonify(respuesta = 'registrado')

@app.route('/sesionv', methods = ['POST'])
def sesionv():
	datos = request.get_json()
	validar = db.session.query(Usuariosv.correo).filter_by(correo = datos['correo']).scalar() is not None
	if validar == None or validar == False:
		return jsonify(respuesta = 'nousuario')
	else:
		validar2 = db.session.query(Usuariosv).filter(Usuariosv.correo == datos['correo']).all()
		session['correo'] = datos['correo']
		for resultado in validar2:
			return jsonify(respuesta = str(resultado.password), nombre = str(resultado.nombre))

@app.route('/usuariosv', methods = ['GET'])
def usuariosv():
	usuarios = db.session.query(Usuariosv).all() #.filter(Usuarios.correo == datos['correo']).first()
	new_usuarios = []

	for x in usuarios:
		new_usuarios.append({"nombre":x.nombre,"correo":x.correo, "fechan":x.fechan, "sexo":x.sexo})

	return jsonify(usuarios = new_usuarios)

@app.route('/winnersv', methods = ['GET'])
def winnersv():
    ganadores = db.session.query(Numerosv).all()
    new_ganadores = []
    for x in ganadores:
        new_ganadores.append({"numero":x.numero,"usuario":x.usuario, "fjugada":x.fjugada, "aciertos":x.aciertos})
        return jsonify(ganadores = new_ganadores)

@app.route('/numerosv', methods = ['POST'])
def numerosv():
	datos = request.get_json()
	now = datetime.now()
	fecha = now.date()
	numero = Numeros(numero = datos['numero'], usuario = datos['correo'], fjugada = fecha, aciertos = datos['puntos'])
	db.session.add(numero)
	db.session.commit()
	return jsonify(respuesta = 'Número registrado satisfactoriamente')

@app.route('/scrapper3v', methods = ['GET'])
def scrapping3v():
	fecha = datetime.now()
	mes = datetime.today() - timedelta(days = 31)
	mes2 = datetime.today() - timedelta(days = 62)
	mes3 = datetime.today() - timedelta(days = 93)
	mes4 = datetime.today() - timedelta(days = 124)
	mes5 = datetime.today() - timedelta(days = 155)
	mes6 = datetime.today() - timedelta(days = 186)
	#mes7 = datetime.today() - timedelta(days = 217)
	g = requests.get('http://m.vincicasa.it/sisal-gn-proxy-servlet-web/proxy/gntn-info-web/rest/gioco/vincicasa/estrazioni/ultimoconcorso?idPartner=MOB_GN_INFO')
	r = requests.get('http://m.vincicasa.it/sisal-gn-proxy-servlet-web/proxy/gntn-info-web/rest/gioco/vincicasa/estrazioni/archivioconcorso/' + str(fecha.year) + '/' + str(fecha.month) + '?idPartner=MOB_GN_INFO')
	r2 = requests.get('http://m.vincicasa.it/sisal-gn-proxy-servlet-web/proxy/gntn-info-web/rest/gioco/vincicasa/estrazioni/archivioconcorso/' + mes.strftime('%Y') + '/' + mes.strftime('%m') + '?idPartner=MOB_GN_INFO')
	r3 = requests.get('http://m.vincicasa.it/sisal-gn-proxy-servlet-web/proxy/gntn-info-web/rest/gioco/vincicasa/estrazioni/archivioconcorso/' + mes2.strftime('%Y') + '/' + mes2.strftime('%m') + '?idPartner=MOB_GN_INFO')
	r4 = requests.get('http://m.vincicasa.it/sisal-gn-proxy-servlet-web/proxy/gntn-info-web/rest/gioco/vincicasa/estrazioni/archivioconcorso/' + mes3.strftime('%Y') + '/' + mes3.strftime('%m') + '?idPartner=MOB_GN_INFO')
	r5 = requests.get('http://m.vincicasa.it/sisal-gn-proxy-servlet-web/proxy/gntn-info-web/rest/gioco/vincicasa/estrazioni/archivioconcorso/' + mes4.strftime('%Y') + '/' + mes4.strftime('%m') + '?idPartner=MOB_GN_INFO')
	r6 = requests.get('http://m.vincicasa.it/sisal-gn-proxy-servlet-web/proxy/gntn-info-web/rest/gioco/vincicasa/estrazioni/archivioconcorso/' + mes5.strftime('%Y') + '/' + mes5.strftime('%m') + '?idPartner=MOB_GN_INFO')
	r7 = requests.get('http://m.vincicasa.it/sisal-gn-proxy-servlet-web/proxy/gntn-info-web/rest/gioco/vincicasa/estrazioni/archivioconcorso/' + mes6.strftime('%Y') + '/' + mes6.strftime('%m') + '?idPartner=MOB_GN_INFO')
	ganadores = requests.get('http://m.vincicasa.it/sisal-gn-proxy-servlet-web/proxy/gntn-info-web/rest/gioco/vincicasa/estrazioni/ultimoconcorso')
	return jsonify(g.text, r.text, r2.text, r3.text, r4.text, r5.text, r6.text, r7.text, ganadores.text)

@app.route('/recuperarv', methods = ['POST'])
def recuperarv():
	datos = request.get_json()
	correo = datos['correo']
	msg = Message("", sender = "chancemilliondayvincicasa@gmail.com", recipients = [correo])
	msg.html = '<a href="http://axelrace.pythonanywhere.com/passwordv">Clicca qui per recuperare la tua password</a>'
	mail.send(msg)
	return jsonify('Mensaje enviado exitosamente')

@app.route('/passwordv')
def passwordv():
    return render_template('recuperarv.html')

@app.route('/cambiov', methods = ['POST'])
def cambiov():
	datos = request.get_json()
	validar = db.session.query(Usuariosv.correo).filter_by(correo = datos['correo']).scalar() is not None
	if validar == None or validar == False:
		return jsonify(respuesta = 'nousuario')
	else:
		db.session.query(Usuariosv).filter(Usuariosv.correo == datos['correo']).update(dict(password = datos['password']))
		db.session.commit()
		return jsonify('Cambio realizado exitosamente')

@app.route('/ganadorv', methods = ['POST'])
def ganadorv():
	datos = request.get_json()
	msg = Message("L'utente " + datos["usuario"] + " ha vinto con " + datos["puntos"] + " punti", sender = "chancemilliondayvincicasa@gmail.com", recipients = ['chancemilliondayvincicasa@gmail.com'])
	mail.send(msg)
	msg = Message("Congratulazioni! hai vinto alla lotteria con " + datos["puntos"] + " punti", sender = "chancemilliondayvincicasa@gmail.com", recipients = [datos["correo"]])
	mail.send(msg)
	return jsonify('Mensajes enviados exitosamente')

@app.route('/pagov', methods = ['GET', 'POST'])
def pagov():
    if request.method == 'POST':
    	datos = request.get_json()
    	now = datetime.now()
    	fecha = now.date()
    	pago = Pago(usuario = datos['usuario'], correo = datos['correo'], fecha = fecha, monto = datos['monto'])
    	db.session.add(pago)
    	db.session.commit()
    	return jsonify('Pago registrado')
    else:
        donadores = db.session.query(Pago).all()
        new_donadores = []
        for x in donadores:
            new_donadores.append({"correo":x.correo,"usuario":x.usuario, "fecha":x.fecha, "monto":x.monto})
        return jsonify(donadores = new_donadores)

if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)