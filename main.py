import io
import os
import sys
from contextlib import redirect_stdout
from flask import Flask, request, jsonify, make_response
import traceback
import threading


def get_output(script, inp, timeout=5):
    output = []

    def run_code():
        try:
            with io.StringIO() as buf, redirect_stdout(buf):
                inpt = io.StringIO(str(inp))
                sys.stdin = inpt
                code = compile(script, '<string>', 'exec')
                d = dict(locals(), **globals())
                exec(code, d, d)
                output.append(buf.getvalue())
        except Exception as error:
            output.append(''.join(traceback.format_exception(None, error, error.__traceback__)))
        finally:
            sys.stdout = sys.__stdout__
            sys.stdin = sys.__stdin__

    thread = threading.Thread(target=run_code)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        return "Error: Code execution timed out"
    else:
        return output[0]


app = Flask(__name__)


@app.route('/runCode', methods=['POST', 'OPTIONS'])
@app.route('/runCode', methods=['POST', 'OPTIONS'])
def runCode():
    if request.method == "OPTIONS":
        return build_cors_preflight_response()
    elif request.method == "POST":
        script = request.json['script']
        inputs = request.json['inputs']

        outputs = []
        for input_data in inputs:
            try:
                output = get_output(script, input_data)
                outputs.append(output)
            except Exception as e:
                outputs.append(str(e))

        response = jsonify({"outputs": outputs})
        return corsify_actual_response(response)


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
