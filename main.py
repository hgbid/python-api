import json
from flask import Flask, request
import io
from contextlib import redirect_stdout


app = Flask(__name__)

def serialize(data):
    return json.dumps(data).replace("null", "None")

@app.route('/runCode', methods=['POST'])
def runCode():
    script = request.json['script']
    input_data = request.json['input']
    print("run code called")

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
    return {"output": output, "massage":massage}

if __name__ == '__main__':
    app.run()
