from flask import Flask, request, jsonify, session, render_template
import pymysql
from flask_cors import CORS
import os
from flask_sqlalchemy import SQLAlchemy
from orm import Numeros, Usuarios
from datetime import datetime, date
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost:3306/landroid?charset=utf8mb4"
db = SQLAlchemy(app)
CORS(app)
app.config['SECRET_KEY'] = 'T1BJXrQJa2eoUf0pA/gu19CbdS0uM='

@app.route('/registro', methods = ['POST'])
def registro():
	datos = request.get_json()
	validar = db.session.query(Usuarios.correo).filter_by(correo = datos['correo']).scalar() is not None
	if validar != None:
		usuario = Usuarios(nombre = datos['nombre'], correo = datos['correo'], fechan = datos['fecha'], password = datos['password'])
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
		validar2 = db.session.query(Usuarios).filter(Usuarios.correo == datos['correo']).all()
		session['correo'] = datos['correo']
		for resultado in validar2:
			return jsonify(respuesta = str(resultado.password))

@app.route('/numeros', methods = ['POST'])
def numeros():
	datos = request.get_json()
	now = datetime.now()
	fecha = now.date()
	numero = Numeros(numero = datos['numero'], usuario = datos['correo'], fjugada = fecha)
	db.session.add(numero)
	db.session.commit()
	return jsonify(respuesta = 'Número registrado satisfactoriamente')

@app.route('/scrapper', methods = ['GET', 'POST'])
def scraping():
	tablas = []
	datas = []
	datas2 = []
	datas3 = []
	chrome_options = webdriver.ChromeOptions()
	chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--disable-dev-shm-usage")
	chrome_options.add_argument("--no-sandbox")
	driver = webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"), chrome_options = chrome_options)
	driver.get('https://www.lottomaticaitalia.it/it/prodotti/millionday')
	datos = driver.find_elements_by_tag_name('td')
	datos2 = driver.find_elements_by_tag_name('span')

	for data in datos:
		datas.append(data.get_attribute("innerHTML"))

	for data in datos2:
		datas2.append(data.get_attribute("innerHTML"))

	for data in range(1, 8):
		datos3 = driver.find_element_by_xpath('/html/body/div/section[2]/div[5]/section/div/div[2]/div[1]/div/div/div/table/tbody/tr[' + str(data) + ']/td[1]')
		datas3.append(datos3.get_attribute("innerHTML")[-5::])
		
	json = {
		'numeros': [{
			'dia1': datas[-6:-1],
			'dia2': datas[-12:-7],
			'dia3': datas[-18:-13],
			'dia4': datas[-24:-19],
			'dia5': datas[-30:-25],
			'dia6': datas[-36:-31],
			'dia7': datas[-42:-37]
		}],
		'fechas': [{
			'dia1': datas3[6],
			'dia2': datas3[5],
			'dia3': datas3[4],
			'dia4': datas3[3],
			'dia5': datas3[2],
			'dia6': datas3[1],
			'dia7': datas3[0]
		}],
		'dias': [{
			'dia1': datas2[26],
			'dia2': datas2[25],
			'dia3': datas2[24],
			'dia4': datas2[23],
			'dia5': datas2[22],
			'dia6': datas2[21],
			'dia7': datas2[20],
		}]
	}
	driver.quit()
	return jsonify(json)
	
#@app.route('/cerrar', methods = ['GET'])
#def cerrar():
#	session.pop('correo', None)
#	return jsonify(respuesta = 'Sesión cerrada exitosamente')

if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)