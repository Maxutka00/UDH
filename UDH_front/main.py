# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
from flask import render_template

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__, template_folder='templates', static_folder='templates')


@app.route('/login')
def login():
    return render_template(
        "login.html")

@app.route('/signup')
def signup():
    return render_template(
        "signup.html")

@app.route('/staties')
def staties():
    return render_template(
        "staties.html")

@app.route('/view_staties')
def view_staties():
    return render_template(
        "view_staties.html")


@app.route('/')
def main():
    return render_template(
        "index.html")


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True, host='0.0.0.0', port=5009, ssl_context='adhoc')
