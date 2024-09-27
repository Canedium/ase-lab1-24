from flask import Flask, request, make_response, jsonify
from functools import reduce
import re,os , threading, signal
app = Flask(__name__, instance_relative_config=True)

@app.route('/add')
def add():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        return make_response(jsonify(s=a+b), 200) #HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400) #HTTP 400 BAD REQUEST

#Endpoint /sub for subtraction which takes a and b as query parameters.
@app.route('/sub')
def sub():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        return make_response(jsonify(s=a-b), 200)
#Endpoint /mul for multiplication which takes a and b as query parameters.
@app.route('/mul')
def mul():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        return make_response(jsonify(s=a*b), 200)
#Endpoint /div for division which takes a and b as query parameters. Returns HTTP 400 BAD REQUEST also for division by zero.
@app.route('/div')
def div():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if not a or not b:
        return make_response('Missing parameters, needs both a and b\n', 400)
    if b == 0:
        return make_response('Division by zero\n', 400)
    return make_response(jsonify(s=a/b), 200)
#Endpoint /mod for modulo which takes a and b as query parameters. Returns HTTP 400 BAD REQUEST also for division by zero.
@app.route('/mod')
def mod():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if not a or not b:
        return make_response('Missing parameters, needs both a and b\n', 400)
    if b == 0:
        return make_response('Division by zero\n', 400)
    return make_response(jsonify(s=a%b), 200)
#Endpoint /random which takes a and b as query parameters and returns a random number between a and b included. Returns HTTP 400 BAD REQUEST if a is greater than b.
@app.route('/random')
def random():
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)
    if a and b:
        if a > b:
            return make_response('a should be less than b\n', 400)
        import random
        return make_response(jsonify(s=random.randint(a, b)), 200)

# /upper which given the string a it returns it in a JSON all in uppercase.
@app.route('/upper')
def upper():
    a = request.args.get('a')
    if a:
        return make_response(jsonify(s=a.upper()), 200)
    else:
        return make_response('Missing parameter a\n', 400)
# /lower which given the string a it returns it in a JSON all in lowercase.
@app.route('/lower')
def lower():
    a = request.args.get('a')
    if a:
        return make_response(jsonify(s=a.lower()), 200)
    else:
        return make_response('Missing parameter a\n', 400)
# /concat which given the strings a and b it returns in a JSON the concatenation of them.
@app.route('/concat')
def concat():
    a = request.args.get('a')
    b = request.args.get('b')
    if a and b:
        return make_response(jsonify(s=a+b), 200)
    else:
        return make_response('Missing parameters a and b\n', 400)
# /reduce which takes the operator op (one of add, sub, mul, div, upper, lower, concat) and a lst string representing a list and apply the operator to all the elements giving the result. For instance, /reduce?op=add&lst=[2,1,3,4] returns a JSON containing {s=10}, meaning 2+1+3+4.
@app.route('/reduce')
def red():
    op = request.args.get('op')
    lst = request.args.get('lst')
    if not op or not lst:
        return make_response('Missing parameters op and lst\n', 400)
    lst = re.sub(r'[\[\]]', '', lst)  # Rimuove le parentesi quadre
    try:
        lst = list(map(float, lst.split(',')))  # Convertire la lista in numeri
    except ValueError:
        return make_response('Invalid list format\n', 400)
    if op == 'add':
        return make_response(jsonify(s=sum(lst)), 200)
    if op == 'sub':
        return make_response(jsonify(s=reduce(lambda x, y: x-y, lst)), 200)
    if op == 'mul':
        return make_response(jsonify(s=reduce(lambda x, y: x*y, lst)), 200)
    if op == 'div':
        return make_response(jsonify(s=reduce(lambda x, y: x/y, lst)), 200)
    if op == 'upper':
        return make_response(jsonify(s=''.join(lst).upper()), 200)
    if op == 'lower':
        return make_response(jsonify(s=''.join(lst).lower()), 200)
    if op == 'concat':
        return make_response(jsonify(s=''.join(lst)), 200)
    return make_response('Invalid operator\n', 400)

# /crash which terminates the service after sending a json containing info about the host and the port of the service.
@app.route('/crash')
def crash():
    threading.Thread(target=kill).start()
    host = request.host.split(':')[0]  
    port = request.host.split(':')[1]  
    response_data = {
        "host": host,
        "port": port
    }
    
    response = make_response(jsonify(response_data), 200)
    return response

def kill():
    os.kill(os.getpid(), signal.SIGINT)
if __name__ == '__main__':
    app.run(debug=True)