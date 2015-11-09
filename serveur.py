#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Daniel-Junior Dubé & Sarah Laflamme'

from bottle import Bottle, route, run, request, response, template, static_file, abort, get, post, parse_auth
from os.path import join, dirname, isfile

appPath = dirname(__file__)

# Static Routes
@route('/<filename:re:.*\.(js|json)>')
def javascripts(filename):
    return static_file(filename, root=join(appPath, 'src', 'js'))

@route('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root=join(appPath, 'src', 'css'))

@route('/<filename:re:.*\.(jpg|png|gif|ico|jpeg)>')
def images(filename):
    return static_file(filename, root=join(appPath, 'src', 'images'))

@route('/<filename:re:.*\.(mp4)>')
def videos(filename):
    return static_file(filename, root=join(appPath, 'src', 'videos'))

@route('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root=join(appPath, 'src', 'fonts'))
    
# Main Route

@route('/')

def main():
    return "Main Page"

@route('/repas')
def main():
    return template(join(appPath, 'base_repas.html'))

@route('/cafe')
def main():
    return template(join(appPath, 'base_cafe.html'))

@route('/dessert')
def main():
    return template(join(appPath, 'base_dessert.html'))

@route('/titre')
def main():
    return template(join(appPath, 'base_titre.html'))

        
if __name__ == "__main__":
    run(host='0.0.0.0', port=8080, debug=True)