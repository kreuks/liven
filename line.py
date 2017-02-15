import os

from flask import Flask

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    return 'Hello stranger\n'


if __name__ == "__main__":
    app.run(
        host=os.environ.get('HOST', None),
        port=int(os.environ.get('PORT', None))
    )
