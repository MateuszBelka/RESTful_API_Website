###############################################################################
# Web Technology at VU University Amsterdam
# Assignment 3
#
# The assignment description is available on Canvas.
# This is a template for you to quickly get started with Assignment 3.
# Read through the code and try to understand it.
#
# Have you looked at the documentation of bottle.py?
# http://bottle.readthedocs.org/en/stable/index.html
#
# Once you are familiar with bottle.py and the assignment, start implementing
# an API according to your design by adding routes.
###############################################################################

# Include more methods/decorators as you use them
# See http://bottle.readthedocs.org/en/stable/api.html#bottle.Bottle.route

from bottle import response, error, get, post, put, delete, request
import json


###############################################################################
# Routes
#
# TODO: Add your routes here and remove the example routes once you know how
#       everything works.
###############################################################################

@get('/retrieve')
def database(db):
    db.execute("SELECT * FROM inventory")
    products = db.fetchall()

    if (products == []):
        response.status_code = 404
        response.content_type = 'application/json'
        response_body = {'Status': 'Not Found', 'message': 'The requested product is not found in the database.'}

    else:
        response.status_code = 200
        response.content_type = 'application/json'
        response_body = products

    response.body = json.dumps(response_body)
    return response


@get('/retrieve/<id>')
def database(db, id):
    db.execute('SELECT * FROM inventory WHERE id = {}'.format(id))
    products = db.fetchall()

    if (products == []):
        response.status_code = 404
        response.content_type = 'application/json'
        response_body = {'Status': 'Not Found', 'message': 'The requested product is not found in the database.'}

    else:
        response.status_code = 200
        response.content_type = 'application/json'
        response_body = products[0]

    response.body = json.dumps(response_body)
    return response

@post('/create')
def database(db):

    product = request.json.get('product')
    origin = request.json.get('origin')
    best_before_date = request.json.get('best_before_date')
    amount = request.json.get('amount')
    image = request.json.get('image')

    if (not product or not origin or not best_before_date or not amount or not image):
        response.status_code = 404
        response.content_type = 'application/json'
        response_body = {'Status': 'Bad Request', 'message': 'The product does not include enough parameters.'}

    else:
        db.execute(INSERT INTO inventory (product, origin, best_before_date, amount, image), VALUES(?, ?, ?, ?, ?), (product, origin, best_before_date, amount, image))
        id = db.lastrowid
        host = request.get_header('host')
        response.status_code = 201
        response.content_type = 'application/json'
        response_body = {'url': 'http://{}/products/{}'.format(host,id)}

    response.body = json.dumps(response_body)
    return response
@put('/update/<id>')


@delete('/reset')







###############################################################################
# Error handling
#
# TODO (optional):
#       Add sensible error handlers for all errors that may occur when a user
#       accesses your API.
###############################################################################


###############################################################################
# This starts the server
#
# Access it at http://localhost:8080
#
# If you have problems with the reloader (i.e. your server does not
# automatically reload new code after you save this file), set `reloader=False`
# and reload manually.
#
# You might want to set `debug=True` while developing and/or debugging and to
# `False` before you submit.
#
# The installed plugin 'WtPlugin' takes care of enabling CORS (Cross-Origin
# Resource Sharing; you need this if you use your API from a website) and
# provides you with a database cursor.
###############################################################################

if __name__ == "__main__":
    from bottle import install, run
    from wtplugin import WtDbPlugin, WtCorsPlugin

    install(WtDbPlugin())
    install(WtCorsPlugin())
    run(host='localhost', port=8080, reloader=True, debug=True, autojson=False)
