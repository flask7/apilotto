from flask import Flask, request, jsonify, session, render_template
import pymysql
from flask_cors import CORS
import os
from flask_sqlalchemy import SQLAlchemy
from orm import Numeros, Usuarios
from datetime import datetime, date
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

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
def scrapping():
	json = {
	  "dias": [
	    {
	      "dia1": "DOMENICA", 
	      "dia2": "SABATO", 
	      "dia3": "VENERD\u00cc", 
	      "dia4": "GIOVED\u00cc", 
	      "dia5": "MERCOLED\u00cc", 
	      "dia6": "MARTED\u00cc", 
	      "dia7": "LUNED\u00cc"
	    }
	  ], 
	  "fechas": [
	    {
	      "dia1": "26/07", 
	      "dia2": "25/07", 
	      "dia3": "24/07", 
	      "dia4": "23/07", 
	      "dia5": "22/07", 
	      "dia6": "21/07", 
	      "dia7": "20/07"
	    }
	  ], 
	  "numeros": [
	    {
	      "dia1": [
	        "17", 
	        "20", 
	        "26", 
	        "49", 
	        "55"
	      ], 
	      "dia2": [
	        "6", 
	        "10", 
	        "15", 
	        "49", 
	        "55"
	      ], 
	      "dia3": [
	        "12", 
	        "15", 
	        "24", 
	        "42", 
	        "48"
	      ], 
	      "dia4": [
	        "8", 
	        "15", 
	        "22", 
	        "28", 
	        "29"
	      ], 
	      "dia5": [
	        "1", 
	        "8", 
	        "9", 
	        "10", 
	        "50"
	      ], 
	      "dia6": [
	        "25", 
	        "32", 
	        "42", 
	        "54", 
	        "55"
	      ], 
	      "dia7": [
	        "8", 
	        "24", 
	        "26", 
	        "34", 
	        "55"
	      ]
	    }
	  ]
	}
	return jsonify(json)

@app.route('/scrapperp', methods = ['GET', 'POST'])
def scrapingp():
	tablas = []
	datas = []
	datas2 = []
	datas3 = []
	driver = webdriver.Chrome(ChromeDriverManager().install())
	driver.implicitly_wait(60)
	driver.get('https://www.lottomaticaitalia.it/it/prodotti/millionday')
	
	for data in range(1,8):
		time.sleep(1)
		for x in range(2,7):
			info = driver.find_element_by_css_selector('body > div > section.container.main-container > div.ltmit-squared-grid > section > div > div.col-sm-4 > div.ltmit-estrazioni-ultime-oggi > div > div > div > table > tbody > tr:nth-child(' + str(data) + ') > td:nth-child(' + str(x) + ')')
			datas.append(info.get_attribute("innerHTML"))

	for data in range(1,8):
		time.sleep(1)
		info = driver.find_element_by_css_selector('body > div > section.container.main-container > div.ltmit-squared-grid > section > div > div.col-sm-4 > div.ltmit-estrazioni-ultime-oggi > div > div > div > table > tbody > tr:nth-child(' + str(data) + ') > td.date.ng-binding > span')
		datas2.append(info.get_attribute("innerHTML"))
	
	for data in range(1,8):
		time.sleep(1)
		info = driver.find_element_by_css_selector('body > div > section.container.main-container > div.ltmit-squared-grid > section > div > div.col-sm-4 > div.ltmit-estrazioni-ultime-oggi > div > div > div > table > tbody > tr:nth-child(' + str(data) + ') > td.date.ng-binding')
		datas3.append(info.get_attribute("innerHTML")[-5::])

	driver.quit()
	
	json = {
		'numeros': [{
			'dia1': datas[0:5],
			'dia2': datas[5:10],
			'dia3': datas[10:15],
			'dia4': datas[15:20],
			'dia5': datas[20:25],
			'dia6': datas[25:30],
			'dia7': datas[30:35]
		}],
		'fechas': [{
			'dia1': datas3[0],
			'dia2': datas3[1],
			'dia3': datas3[2],
			'dia4': datas3[3],
			'dia5': datas3[4],
			'dia6': datas3[5],
			'dia7': datas3[6]
		}],
		'dias': [{
			'dia1': datas2[0],
			'dia2': datas2[1],
			'dia3': datas2[2],
			'dia4': datas2[3],
			'dia5': datas2[4],
			'dia6': datas2[5],
			'dia7': datas2[6]
		}]
	}
	
	return jsonify(json)
	
@app.route('/scrapper2', methods = ['GET'])
def scrapper2():
	tablas = []
	datas = []
	datas2 = []
	datas3 = []
	driver = webdriver.Chrome(ChromeDriverManager().install())
	driver.implicitly_wait(30)
	driver.get('https://www.lottomaticaitalia.it/it/prodotti/millionday/estrazioni')
	
	for data in range(1,30):
		time.sleep(1)
		for x in range(2,7):
			info = driver.find_element_by_css_selector('body > div > section.container.main-container > div.ltmit-archivio-estrazioni > div > div.col-xs-12.col-sm-8.col-sm-push-4 > table > tbody > tr:nth-child(' + str(data) + ') > td:nth-child(' + str(x) + ')')
			datas.append(info.get_attribute("innerHTML"))

	for data in range(1,30):
		time.sleep(1)
		info = driver.find_element_by_css_selector('body > div > section.container.main-container > div.ltmit-archivio-estrazioni > div > div.col-xs-12.col-sm-8.col-sm-push-4 > table > tbody > tr:nth-child(' + str(data) + ') > td.date.ng-binding > span')
		datas2.append(info.get_attribute("innerHTML"))
	
	for data in range(1,30):
		time.sleep(1)
		info = driver.find_element_by_css_selector('body > div > section.container.main-container > div.ltmit-archivio-estrazioni > div > div.col-xs-12.col-sm-8.col-sm-push-4 > table > tbody > tr:nth-child(' + str(data) + ') > td.date.ng-binding')
		datas3.append(info.get_attribute("innerHTML")[-31:-16])

	driver.quit()
	
	json = {
		'numeros': [{
			'dia1': datas[0:5],
			'dia2': datas[5:10],
			'dia3': datas[10:15],
			'dia4': datas[15:20],
			'dia5': datas[20:25],
			'dia6': datas[25:30],
			'dia7': datas[30:35],
			'dia8': datas[35:40],
			'dia9': datas[40:45],
			'dia10': datas[45:50],
			'dia11': datas[50:55],
			'dia12': datas[55:60],
			'dia13': datas[60:65],
			'dia14': datas[65:70],
			'dia15': datas[70:75],
			'dia16': datas[75:80],
			'dia17': datas[80:85],
			'dia18': datas[85:90],
			'dia19': datas[90:95],
			'dia20': datas[95:100],
			'dia21': datas[100:105],
			'dia22': datas[105:110],
			'dia23': datas[110:115],
			'dia24': datas[115:120],
			'dia25': datas[120:125],
			'dia26': datas[125:130],
			'dia27': datas[130:135],
			'dia28': datas[135:140],
			'dia29': datas[140:145]
		}],
		'fechas': [{
			'dia1': datas3[0],
			'dia2': datas3[1],
			'dia3': datas3[2],
			'dia4': datas3[3],
			'dia5': datas3[4],
			'dia6': datas3[5],
			'dia7': datas3[6],
			'dia8': datas3[7],
			'dia9': datas3[8],
			'dia10': datas3[9],
			'dia11': datas3[10],
			'dia12': datas3[11],
			'dia13': datas3[12],
			'dia14': datas3[13],
			'dia15': datas3[14],
			'dia16': datas3[15],
			'dia17': datas3[16],
			'dia18': datas3[17],
			'dia19': datas3[18],
			'dia20': datas3[19],
			'dia21': datas3[20],
			'dia22': datas3[21],
			'dia23': datas3[22],
			'dia24': datas3[23],
			'dia25': datas3[24],
			'dia26': datas3[25],
			'dia27': datas3[26],
			'dia28': datas3[27],
			'dia29': datas3[28]
		}],
		'dias': [{
			'dia1': datas2[0],
			'dia2': datas2[1],
			'dia3': datas2[2],
			'dia4': datas2[3],
			'dia5': datas2[4],
			'dia6': datas2[5],
			'dia7': datas2[6],
			'dia8': datas2[7],
			'dia9': datas2[8],
			'dia10': datas2[9],
			'dia11': datas2[10],
			'dia12': datas2[11],
			'dia13': datas2[12],
			'dia14': datas2[13],
			'dia15': datas2[14],
			'dia16': datas2[15],
			'dia17': datas2[16],
			'dia18': datas2[17],
			'dia19': datas2[18],
			'dia20': datas2[19],
			'dia21': datas2[20],
			'dia22': datas2[21],
			'dia23': datas2[22],
			'dia24': datas2[23],
			'dia25': datas2[24],
			'dia26': datas2[25],
			'dia27': datas2[26],
			'dia28': datas2[27],
			'dia29': datas2[28]
		}]
	}
	return jsonify(json)

#@app.route('/cerrar', methods = ['GET'])
#def cerrar():
#	session.pop('correo', None)
#	return jsonify(respuesta = 'Sesión cerrada exitosamente')

if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)