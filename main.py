import io
import os
import sys
from contextlib import redirect_stdout
from flask import Flask, request, jsonify, make_response
import traceback

def get_output(script, inp):
    try:
        with io.StringIO() as buf, redirect_stdout(buf):
            inpt = io.StringIO(str(inp))
            sys.stdin = inpt
            code = compile(script, '<string>', 'exec')
            d = dict(locals(), **globals())
            exec(code, d, d)
            output = buf.getvalue()
    except Exception as error:
        output = ''.join(traceback.format_exception(None, error, error.__traceback__))
    finally:
        sys.stdout = sys.__stdout__
        sys.stdin = sys.__stdin__
    return output


app = Flask(__name__)

@app.route('/runCode', methods=['POST', 'OPTIONS'])
def runCode():
    if request.method == "OPTIONS":
        return build_cors_preflight_response()
    elif request.method == "POST":
        script = request.json['script']
        input_data = request.json['input']

        print("run code called")
        print(input_data)    
        try:
            output = get_output(script, input_data)
            massage = "Script executed successfully"
        except Exception as e:
            print(str(e))
            massage=str(e)

        print(output)
        print("run code return output")
        return jsonify({"output": output, "massage":massage})

def build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)