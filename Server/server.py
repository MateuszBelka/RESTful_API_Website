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

from bottle import response, request, error, get, post, put, delete
import json

###############################################################################
# Routes
#
# TODO: Add your routes here and remove the example routes once you know how
#       everything works.
###############################################################################

@get('/retrieve')
def retrieve_db(db):
    items = db.execute("SELECT product, origin, best_before_date, amount, image, id FROM supermarket").fetchall()
    response.content_type = 'application/json'
    response.add_header('Access-Control-Allow-Origin', '*')
    response.add_header('Allow', 'GET, HEAD')
    response.body = json.dumps(items)
    return response

@get('/retrieve/<id>')
def retrieveItem(db, id):
    item = db.execute('SELECT * FROM supermarket WHERE id = ?', (id)).fetchone()
    if item:
        response.status = 200
        response.content_type = 'application/json'
        response_body = item
    else:
        response.status = 404
        response.content_type = 'application/json'
        response_body = {'status': 'Not Found', 'message': 'The database is empty.'}

    response.add_header('Access-Control-Allow-Origin', '*')
    response.add_header('Allow', 'GET, HEAD')
    response.body = json.dumps(response_body)
    return response

@post('/create')
def create(db):
    product = request.json.get('product')
    origin = request.json.get('origin')
    best_before_date = request.json.get('best_before_date')
    amount = request.json.get('amount')
    image = request.json.get('image')

    if (product and origin and best_before_date and amount and image):
        db.execute('INSERT INTO supermarket (product, origin, best_before_date, amount, image) VALUES (?, ?, ?, ?, ?)', (product, origin, best_before_date, amount, image))
        id = db.lastrowid
        response.status = 201
        response.content_type = 'application/json'
        response_body = {'url': 'http://localhost:8080/retrieve/{}'.format(id)}
    else:
        response.status = 400
        response.content_type = 'application/json'
        response_body = {'status': 'Bad Request', 'message': 'You are missing elements in your request.'}

    response.add_header('Access-Control-Allow-Origin', '*')
    response.add_header('Allow', 'POST, HEAD')
    response.body = json.dumps(response_body)
    return response

@put('/update/<id>')
def update(db, id):
    product = request.json.get('product')
    origin = request.json.get('origin')
    best_before_date = request.json.get('best_before_date')
    amount = request.json.get('amount')
    image = request.json.get('image')

    if (product and origin and best_before_date and amount and image):
        item = db.execute('SELECT * FROM supermarket WHERE id = ?', (id)).fetchone()
        if item:
            response_body = db.execute('UPDATE supermarket SET product = ?, origin = ?, best_before_date = ?, amount = ?, image = ? WHERE id = ?', (product, origin, best_before_date, amount, image, id)).fetchone()
            response.status = 201
            response.content_type = 'application/json'
        else:
            response.status = 404
            response.content_type = 'application/json'
            response_body = {'status': 'Not Found', 'message': 'Item you are looking for could not be found.'}
    else:
        response.status = 400
        response.content_type = 'application/json'
        response_body = {'status': 'Bad Request', 'message': 'You are missing elements in your request.'}

    response.add_header('Access-Control-Allow-Origin', '*')
    response.add_header('Allow', 'PUT, HEAD')
    response.body = json.dumps(response_body)
    return response

@delete('/delete/<id>')
def delete(db, id):
    item = db.execute('SELECT * FROM supermarket WHERE id = ?', (id)).fetchone()
    if item:
        db.execute('DELETE FROM supermarket WHERE id = ?', (id))
        response.status = 204
        response.content_type = 'application/json'
        response.body = ''
    else:
        response.status = 400
        response.content_type = 'application/json'
        response_body = {'status': 'Bad Request', 'message': 'You are missing elements in your request.'}
        response.body = json.dumps(response_body)

    response.add_header('Access-Control-Allow-Origin', '*')
    response.add_header('Allow', 'DELETE, HEAD')
    return response
###############################################################################
# Error handling
#
# TODO (optional):
#       Add sensible error handlers for all errors that may occur when a user
#       accesses your API.
###############################################################################

@error(404)
def error404(error):
    response.content_type = 'application/json'
    response.body = json.dumps({'Error':  {'status': error.status, 'message': error.status_line}})
    return response

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
