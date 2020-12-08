from flask import Flask, render_template

from renderer import render_new_map

app = Flask(__name__)


@app.route('/')
def home():
    render_new_map()
    return render_template("map.html")


if __name__ == '__main__':
    app.run(debug=True)
