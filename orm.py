from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@localhost:3306/landroid"
db = SQLAlchemy(app)

class Numeros(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    numero = db.Column(db.String(80), unique = False, nullable = False)
    usuario = db.Column(db.String(64), unique = False, nullable = False)
    fjugada = db.Column(db.Date, unique = True, nullable = False)
    aciertos = db.Column(db.Integer)

class Usuarios(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nombre = db.Column(db.String(250), unique = True, nullable = False)
	correo = db.Column(db.String(250), unique = True, nullable = False)
	fechan = db.Column(db.Date, unique = True, nullable = False)
	password = db.Column(db.String(256), unique = True, nullable = False)
	sexo = db.Column(db.String(10), unique = True, nullable = False)

class Pago(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    correo = db.Column(db.String(250), unique = True, nullable = False)
    usuario = db.Column(db.String(250), unique = True, nullable = False)
    monto = db.Column(db.String(250), unique = True, nullable = False)
    fecha = db.Column(db.Date, unique = True, nullable = False)

class Numerosv(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    numero = db.Column(db.String(80), unique = False, nullable = False)
    usuario = db.Column(db.String(64), unique = False, nullable = False)
    fjugada = db.Column(db.Date, unique = True, nullable = False)
    aciertos = db.Column(db.Integer)

class Usuariosv(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nombre = db.Column(db.String(250), unique = True, nullable = False)
	correo = db.Column(db.String(250), unique = True, nullable = False)
	fechan = db.Column(db.Date, unique = True, nullable = False)
	password = db.Column(db.String(256), unique = True, nullable = False)
	sexo = db.Column(db.String(10), unique = True, nullable = False)

class Pagov(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    correo = db.Column(db.String(250), unique = True, nullable = False)
    usuario = db.Column(db.String(250), unique = True, nullable = False)
    monto = db.Column(db.String(250), unique = True, nullable = False)
    fecha = db.Column(db.Date, unique = True, nullable = False)
