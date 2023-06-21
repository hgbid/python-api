import io
import os
import sys
import json
from contextlib import redirect_stdout
from flask import Flask, request, jsonify, make_response

def serialize(data):
    return json.dumps(data).replace("null", "None")

def get_output(script, inp):
    try:
        with io.StringIO() as buf, redirect_stdout(buf):
            inpt = io.StringIO(inp)
            sys.stdin = inpt
            code = compile(script, '<string>', 'exec')
            d = dict(locals(), **globals())
            exec(code, d, d)
            output = buf.getvalue()
    except Exception as error:
        output = str(error)
    finally:
        sys.stdout = sys.__stdout__
        sys.stdin = sys.__stdin__
    return output


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/runCode', methods=['POST'])
def runCode():
    script = request.json['script']
    input_data = request.json['input']

    print("run code called")
    print(input_data)
    try:
        output = get_output(script, input_data)
        massage = "Script executed successfully"
    except Exception as error:
        print(str(error))
        massage=str(error)

    print(output)
    print("run code return output")
    response = jsonify({"output": output, "massage":massage})
    return corsify_actual_response(response)


def corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    #port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=5000)
