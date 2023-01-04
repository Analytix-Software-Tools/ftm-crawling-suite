from flask import Flask

app = Flask(__name__)

@app.get('/raw_data')
def get_raw_data():
    pass