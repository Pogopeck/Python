import os
import subprocess
from flask import Flask, render_template

app = Flask(__name__)

scripts = [
    "aws_dsf.py",
    "dsf_sanity.py",
    "FMEnt.py",
    "ITAd.py",
    "OPent.py",
    "pega_dsf.py",
    "TParty.py"
]

# Path to your virtual environment's Python executable
python_executable = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")

@app.route('/')
def index():
    return render_template('index.html', scripts=scripts)

@app.route('/run/<script_name>')
def run_script(script_name):
    script_path = os.path.join(os.getcwd(), script_name)
    try:
        subprocess.run([python_executable, script_path], check=True)
        return f"✅ Successfully ran {script_name}"
    except subprocess.CalledProcessError:
        return f"❌ Failed to run {script_name}"
    except FileNotFoundError:
        return f"🚫 Script not found: {script_name}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
