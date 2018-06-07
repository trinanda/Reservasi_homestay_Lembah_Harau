# import sys, os
#
# from flask import Flask
#
# sys.path.append(os.getcwd() + '/web_app') #sesuai dengan mark directory as sources
#
# app = Flask(__name__)
# app.config.from_pyfile('settings.py')
#
# from models import database
# database2 = database
#
# from geoalchemy2.types import Geometry
# class Point(database2.Model):
#     id = database2.Column(database2.Integer, primary_key=True)
#     name = database2.Column(database2.String(64), unique=True)
#     point = database2.Column(Geometry("POINT"))
#
# database2.create_all()
