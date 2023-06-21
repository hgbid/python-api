import io
import os
from contextlib import redirect_stdout
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

@app.route('/runCode', methods=['POST', 'OPTIONS'])
def runCode():
    if request.method == "OPTIONS":
        return build_cors_preflight_response()
    elif request.method == "POST":
        script = request.json['script']
        input_data = request.json['input']
        print("run code called")
        print(script)
        print(input_data)
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            try:
                exec(script, {"input": lambda: input_data})
                massage = "Script executed successfully"
            except Exception as e:
                print(str(e))
                massage=str(e)

        output = output_buffer.getvalue()
        print("run code return output")
        response = jsonify({"output": output, "massage":massage})
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
