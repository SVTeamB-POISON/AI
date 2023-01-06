from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def test():
    return "hello"

if __name__ == '__main__':
    app.run()