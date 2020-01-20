from flask import Flask
app = Flask(__name__)

@app.route('/dne')
def test_route():
    return 'site wil be here\n'
